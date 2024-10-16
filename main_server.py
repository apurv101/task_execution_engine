# main_server.py

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, field_validator
from typing import List
import uuid
import os
import io
from PIL import Image
import asyncio
from datetime import datetime, timezone

# from vision_system_backend import VisionSystem
# from llm_interface_backend import LLMInterface
from mock_vision_system_backend import VisionSystem
from mock_llm_interface_backend import LLMInterface
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection URI
MONGODB_URI = os.getenv("MONGODB_URI", "your-default-mongodb-uri")
DATABASE_NAME = "amyable_db"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    print("Starting up...")
    # Ensure the database connection is alive
    try:
        app.mongodb_client = AsyncIOMotorClient(MONGODB_URI)
        app.db = app.mongodb_client[DATABASE_NAME]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Could not connect to MongoDB") from e

    # Initialize Vision System and LLM Interface
    cwd = os.getcwd()
    google_credentials_path = f"{cwd}/{os.getenv('GOOGLE_CREDENTIALS_PATH')}"
    yolo_model_path = f"{cwd}/{os.getenv('YOLO_MODEL_PATH')}"

    app.llm_interface = LLMInterface(api_key=os.getenv("OPENAI_API_KEY"))
    app.vision_system = VisionSystem(google_credentials_path, yolo_model_path)

    yield  # The app runs here

    # Shutdown tasks
    print("Shutting down...")
    app.mongodb_client.close()

app = FastAPI(title="AI Server", version="1.0.0", lifespan=lifespan)

# CORS middleware (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request and response validation
class TaskRequest(BaseModel):
    task_description: str

class InstructionResponse(BaseModel):
    instruction_id: str
    instruction_description: str
    status: str
    updated_at: datetime

class TaskResponse(BaseModel):
    task_id: str
    instructions: List[InstructionResponse]

class UpdateInstructionStatusRequest(BaseModel):
    instruction_id: str = Field(..., description="Unique identifier of the instruction")
    status: str = Field(..., description='New status of the instruction ("completed" or "failed")')

    @field_validator('status')
    def validate_status(cls, v):
        allowed_statuses = {"completed", "failed"}
        if v not in allowed_statuses:
            raise ValueError(f'status must be one of {allowed_statuses}')
        return v

class UpdateInstructionStatusResponse(BaseModel):
    instruction_id: str
    status: str
    message: str

# ---------------
# Helper Functions
# ---------------

# Database Operations

async def insert_instructions(db, instructions):
    """Insert multiple instructions into the instructions collection."""
    await db["instructions"].insert_many(instructions)

async def insert_task(db, task):
    """Insert a task into the tasks collection."""
    await db["tasks"].insert_one(task)

async def find_instruction(db, instruction_id):
    """Find an instruction by instruction_id."""
    return await db["instructions"].find_one({"instruction_id": instruction_id})

async def update_instruction_action_history(db, instruction_id, action_history):
    """Update the action history and updated_at of an instruction."""
    await db["instructions"].update_one(
        {"instruction_id": instruction_id},
        {"$set": {
            "action_history": action_history,
            "updated_at": datetime.now(timezone.utc)
        }},
    )

async def update_instruction_status_instructions(db, instruction_id, status):
    """Update the status and updated_at of an instruction in the instructions collection."""
    result = await db["instructions"].update_one(
        {"instruction_id": instruction_id},
        {"$set": {
            "status": status,
            "updated_at": datetime.now(timezone.utc)
        }}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Instruction ID not found in instructions collection")

async def update_instruction_status_tasks(db, instruction_id, status):
    """Update the status and updated_at of an instruction within the tasks collection."""
    result = await db["tasks"].update_one(
        {"instructions.instruction_id": instruction_id},
        {"$set": {
            "instructions.$.status": status,
            "instructions.$.updated_at": datetime.now(timezone.utc)
        }}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Instruction ID not found in tasks collection")

async def update_instruction_status_in_db(db, instruction_id, status):
    """Update instruction status in both instructions and tasks collections."""
    await update_instruction_status_instructions(db, instruction_id, status)
    await update_instruction_status_tasks(db, instruction_id, status)

# External Service Calls

async def decompose_task(llm_interface: LLMInterface, task_description):
    """Use the LLM to decompose the task into instructions."""
    return await llm_interface.decompose_task(task_description)

async def generate_next_action(llm_interface: LLMInterface, instruction_description, google_elements, yolo_elements, action_history, image):
    """Generate the next action using the LLM interface."""
    return await llm_interface.generate_next_action(
        task=instruction_description,
        google_vision_elements=google_elements,
        yolo_elements=yolo_elements,
        action_history=action_history,
        image=image
    )

def process_image(vision_system: VisionSystem, image):
    """Process the image using the vision system."""
    google_vision_elements = vision_system.detect_text(image)
    yolo_elements = vision_system.yolo_service(image)
    return google_vision_elements, yolo_elements

# ---------------
# API Endpoints
# ---------------

@app.post("/add_task", response_model=TaskResponse)
async def add_task(task_request: TaskRequest):
    """
    Endpoint to add a new task.
    Receives a task description, decomposes it into instructions using LLM,
    stores the task and instructions in MongoDB, and returns the task_id and instructions.
    """
    try:
        # Generate a unique task_id
        task_id = str(uuid.uuid4())

        # Use LLM to decompose the task into instructions
        instructions_list = await decompose_task(app.llm_interface, task_request.task_description)

        # Prepare instructions for insertion into MongoDB
        instructions = []
        now = datetime.now(timezone.utc)
        for instr_desc in instructions_list:
            instruction_id = str(uuid.uuid4())
            instruction = {
                "instruction_id": instruction_id,
                "task_id": task_id,
                "instruction_description": instr_desc,
                "action_history": [],
                "status": "pending",
                "created_at": now,
                "updated_at": now
            }
            instructions.append(instruction)

        # Insert instructions into the 'instructions' collection
        await insert_instructions(app.db, instructions)

        # Prepare task document
        task = {
            "task_id": task_id,
            "description": task_request.task_description,
            "instructions": [
                {
                    "instruction_id": instr["instruction_id"],
                    "status": instr["status"],
                    "updated_at": instr["updated_at"]
                } for instr in instructions
            ],
            "created_at": now,
            "updated_at": now
        }

        # Insert the task into the 'tasks' collection
        await insert_task(app.db, task)

        # Prepare response
        response = {
            "task_id": task_id,
            "instructions": [
                {
                    "instruction_id": instr["instruction_id"],
                    "instruction_description": instr["instruction_description"],
                    "status": instr["status"],
                    "updated_at": instr["updated_at"]
                } for instr in instructions
            ]
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_actions")
async def generate_actions(
    screenshot: UploadFile = File(...),
    instruction_id: str = Form(...)
):
    """
    Process the screenshot and generate actions.
    """
    try:
        # Read the image data
        image_data = await screenshot.read()
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file") from e

    # Fetch instruction from the database
    instruction = await find_instruction(app.db, instruction_id)
    if not instruction:
        raise HTTPException(status_code=404, detail="Instruction ID not found")

    # Get action history and instruction description
    action_history = instruction.get("action_history", [])
    instruction_description = instruction.get("instruction_description", "")

    # Process the image using the vision system
    google_vision_elements, yolo_elements = process_image(app.vision_system, image)

    # Generate next actions using LLM
    action = await generate_next_action(
        app.llm_interface,
        instruction_description,
        google_vision_elements,
        yolo_elements,
        action_history,
        image
    )

    # Update action history
    action_history.extend(action['actions'])

    # Update instruction in the database
    await update_instruction_action_history(app.db, instruction_id, action_history)

    # Prepare response
    response = {
        "instruction_id": instruction_id,
        "actions": action['actions'],
    }

    return response

@app.post("/update_instruction_status", response_model=UpdateInstructionStatusResponse)
async def update_instruction_status(update_request: UpdateInstructionStatusRequest):
    """
    Endpoint to update the status of an instruction.
    Receives an instruction_id and a new status ("completed" or "failed"),
    updates the instruction in both instructions and tasks collections,
    and returns a confirmation message.
    """
    try:
        instruction_id = update_request.instruction_id
        status = update_request.status

        # Update instruction status in the database
        await update_instruction_status_in_db(app.db, instruction_id, status)

        # Prepare response
        response = UpdateInstructionStatusResponse(
            instruction_id=instruction_id,
            status=status,
            message=f"Instruction {instruction_id} status updated to '{status}'."
        )

        return response

    except HTTPException as he:
        # Re-raise HTTPExceptions for FastAPI to handle
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))