# main_server.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional
import uuid
import os
import io
from PIL import Image
import asyncio

from vision_system_backend import VisionSystem
from llm_interface_backend import LLMInterface
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    print("Starting up...")
    # Ensure the database connection is alive
    # try:
    #     await client.server_info()
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail="Could not connect to MongoDB") from e
    
    yield  # The app runs here
    
    # Shutdown tasks
    print("Shutting down...")
    # client.close()

app = FastAPI(title="AI Server", version="1.0.0", lifespan=lifespan)

# CORS middleware (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection URI
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = "ai_server_db"

# Initialize MongoDB client
# client = AsyncIOMotorClient(MONGODB_URI)
# db = client[DATABASE_NAME]

client = None
db = None

cwd = os.getcwd()

google_credentials_path = f"{cwd}/{os.getenv("GOOGLE_CREDENTIALS_PATH")}"
yolo_model_path = f"{cwd}/{os.getenv("YOLO_MODEL_PATH")}"

# Initialize Vision System and LLM Interface
llm_interface = LLMInterface(api_key=os.getenv("OPENAI_API_KEY"))
vision_system = VisionSystem(google_credentials_path, yolo_model_path)

class Action(BaseModel):
    action_type: str
    description: str
    clickable_coordinates: Optional[list]
    # Add other fields as necessary

class Task(BaseModel):
    task_id: str
    task_description: str
    actions: list

@app.post("/generate_actions")
async def generate_actions(
    screenshot: UploadFile = File(...),
    task_description: str = Form(...),
    task_id: Optional[str] = Form(None)
):
    """
    Process the screenshot and generate actions.

    - If task_id is None, create a new task.
    - If task_id exists, retrieve previous actions.
    """
    try:
        # Read the image data
        image_data = await screenshot.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file") from e

    # Handle task ID
    if not task_id:
        # New task
        task_id = str(uuid.uuid4())
        is_new_task = True
    else:
        # Existing task
        is_new_task = False

    # Retrieve action history
    if is_new_task:
        action_history = []
    else:
        # Fetch previous actions from the database
        task = await db.tasks.find_one({"task_id": task_id})
        if not task:
            raise HTTPException(status_code=404, detail="Task ID not found")
        action_history = task.get("actions", [])

    # Process the image (vision system) parallel
    # google_task = asyncio.create_task(vision_system.detect_text(image))
    # yolo_task = asyncio.create_task(vision_system.yolo_service(image))

    # google_vision_elements, yolo_elements = await asyncio.gather(google_task, yolo_task)

    # Process the image (vision system) serially
    google_vision_elements = vision_system.detect_text(image)
    yolo_elements = vision_system.yolo_service(image)

    # Generate next actions using LLM
    action = await llm_interface.generate_next_action(
        task=task_description,
        google_vision_elements=google_vision_elements,
        yolo_elements=yolo_elements,
        action_history=action_history,
        image=image
    )

    # Update action history
    action_history.extend(action['actions'])

    # Upsert task in the database
    await db.tasks.update_one(
        {"task_id": task_id},
        {"$set": {
            "task_description": task_description,
            "actions": action_history
        }},
        upsert=True
    )

    # Prepare response
    response = {
        "task_id": task_id,
        "actions": [action],
    }

    return response

# @app.on_event("startup")
# async def startup_event():
#     """Handle startup events such as database connections."""
#     # Ensure the database connection is alive
#     try:
#         await client.server_info()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Could not connect to MongoDB") from e

# @app.on_shutdown
# async def shutdown_event():
#     """Handle shutdown events such as closing database connections."""
#     client.close()