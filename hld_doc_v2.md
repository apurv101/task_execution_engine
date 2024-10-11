# Amyable High-Level Design Document

## Table of Contents

1. [Introduction](#introduction)
2. [System Overview](#system-overview)
3. [Architecture Diagram](#architecture-diagram)
4. [Components Description](#components-description)
   - [Desktop Application](#desktop-application)
   - [Backend Server](#backend-server)
   - [MongoDB Database](#mongodb-database)
5. [Workflow](#workflow)
6. [Technology Stack](#technology-stack)
7. [Data Storage](#data-storage)
8. [APIs](#apis)
9. [Error Handling and Logging](#error-handling-and-logging)
10. [Security Considerations](#security-considerations)
11. [Scalability and Performance](#scalability-and-performance)
12. [Conclusion](#conclusion)

---

## Introduction

Amyable is a task automation application designed to perform tasks on a host machine by interpreting the current screen's state and executing the next set of actions. It leverages computer vision and natural language processing to understand the GUI elements and determine the appropriate actions to achieve the desired tasks.

---

## System Overview

The system comprises three main components:

1. **Desktop Application**: An executable running on the host machine where tasks are performed.

2. **Backend Server**: A RESTful API server that processes task descriptions and screenshots to determine the next actions.

3. **MongoDB Database**: Stores tasks, instructions, and action histories for the application.

The core functionality involves capturing the current screen, interpreting GUI elements using Google Vision and YOLO models, determining next actions using a Large Language Model (LLM), and executing those actions via `pyautogui`.

---

## Architecture Diagram

*Note: Please insert an updated architecture diagram reflecting the new components and workflows.*

---

## Components Description

### Desktop Application

- **Function**: Retrieves pending instructions from MongoDB, captures screenshots, communicates with the backend server, and executes the received actions.

- **Technologies**:
  - Python
  - `pyautogui` for automating GUI interactions
  - MongoDB driver for accessing the database

- **Responsibilities**:
  - Retrieve the next pending instruction from the `instructions` collection.
  - Update the status of the instruction to "in-progress".
  - Capture the current screen state.
  - Send instruction IDs and screenshots to the backend server.
  - Execute actions received from the backend server.
  - Update the status of the instruction to "completed" or "failed" based on execution outcome.

### Backend Server

- **Function**: Processes incoming task descriptions and screenshots to generate the next actions, manages tasks and instructions in MongoDB.

- **Technologies**:
  - Python
  - FastAPI for building RESTful APIs
  - Google Vision API for text detection
  - YOLO model for object detection
  - OpenAI API for LLM integration
  - MongoDB for storing tasks, instructions, and action histories

- **Responsibilities**:
  - Receive task descriptions via API and create tasks and instructions.
  - Use LLM to break down tasks into instructions.
  - Store tasks and instructions in MongoDB.
  - Receive instruction IDs and screenshots from the desktop application.
  - Use computer vision to interpret GUI elements.
  - Utilize LLM to determine the next actions.
  - Update action history in MongoDB.
  - Respond with the next actions to the desktop application.

### MongoDB Database

- **Function**: Stores tasks, instructions, and action histories for the application.

- **Technologies**:
  - MongoDB
  - `motor` (async MongoDB driver for Python)

- **Responsibilities**:
  - Store main tasks with their descriptions and list of instruction IDs.
  - Store instructions with their descriptions, statuses, and action histories.
  - Provide efficient querying mechanisms for retrieving pending instructions.
  - Ensure data consistency and integrity.

---

## Workflow

### Adding a New Task

1. **Task Submission**:

   - The backend server receives a task description via the API.

2. **Task Decomposition**:

   - The backend server uses the LLM to generate instructions based on the main task description.

3. **Database Insertion**:

   - Inserts the main task into the `tasks` collection.
   - Inserts instructions into the `instructions` collection, referencing the `task_id`.

### Desktop Application Processing

1. **Instruction Retrieval**:

   - The desktop application queries the `instructions` collection to get the next instruction with `status: "pending"` for a specific `task_id`.
   - Updates the status of the instruction to "in-progress".

2. **Action Execution**:

   - The desktop application calls the backend server with the `instruction_id` and the current screenshot.
   - Executes the received actions using `pyautogui`.

3. **Instruction Completion**:

   - Updates the instruction’s status to "completed" upon success or "failed" upon failure in MongoDB.

### Backend Server Interaction

1. **Action Generation**:

   - Upon receiving the `instruction_id` and screenshot from the desktop application, the backend server retrieves the instruction from the `instructions` collection, including its `action_history`.

2. **GUI Element Detection**:

   - Uses the Vision System to detect text (Google Vision API) and GUI elements (YOLO model) from the screenshot.

3. **Next Actions Determination**:

   - The LLM Interface processes the instruction description, detected GUI elements, and action history to generate the next actions.

4. **Action History Update**:

   - Updates the `action_history` for the instruction in the `instructions` collection.

5. **Response to Desktop Application**:

   - Sends the next actions back to the desktop application.

---

## Technology Stack

- **Programming Language**: Python
- **Desktop Automation**: `pyautogui`
- **Web Framework**: FastAPI
- **Computer Vision**:
  - Google Vision API (Text Detection)
  - YOLO Model (Object Detection)
- **Natural Language Processing**:
  - OpenAI's GPT-4 (LLM)
- **Database**: MongoDB
- **Asynchronous Programming**: `asyncio`, `httpx`
- **Environment Management**: `python-dotenv` for environment variables
- **Data Serialization**: JSON

---

## Data Storage

- **Database**: MongoDB

### Purpose

- Store main tasks, instructions, action histories, and their statuses.
- Enable retrieval and updating of tasks and instructions for processing.

### Collections

#### `tasks` Collection

```json
{
  "_id": ObjectId("..."),
  "task_id": "unique-task-id",
  "description": "Main task description",
  "instructions": [
    {
      "instruction_id": "instruction-id-1",
      "status": "pending",
      "updated_at": ISODate("...")
    },
    // ... other instructions
  ],
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

- **Fields**:
  - `_id`: MongoDB's unique identifier.
  - `task_id`: Unique identifier for the main task.
  - `description`: Description of the main task.
  - `instructions`: Array of instruction references.
    - `instruction_id`: Unique identifier for the instruction.
    - `status`: Current status of the instruction.
    - `updated_at`: Timestamp of the last update.
  - `created_at`: Timestamp when the task was created.
  - `updated_at`: Timestamp when the task was last updated.

#### `instructions` Collection

```json
{
  "_id": ObjectId("..."),
  "instruction_id": "instruction-id-1",
  "task_id": "unique-task-id",
  "instruction_description": "Instruction description",
  "action_history": [
    // List of actions performed
  ],
  "status": "pending",
  "created_at": ISODate("..."),
  "updated_at": ISODate("...")
}
```

- **Fields**:
  - `_id`: MongoDB's unique identifier.
  - `instruction_id`: Unique identifier for the instruction.
  - `task_id`: Reference to the parent task.
  - `instruction_description`: Description of the instruction.
  - `action_history`: List of actions performed for the instruction.
  - `status`: Current status of the instruction (`pending`, `in-progress`, `completed`, `failed`).
  - `created_at`: Timestamp when the instruction was created.
  - `updated_at`: Timestamp when the instruction was last updated.

### Indexes

- **`tasks` Collection**:
  - Index on `task_id` (unique).
- **`instructions` Collection**:
  - Index on `instruction_id` (unique).
  - Index on `task_id` to enable efficient retrieval of instructions for a given task.
  - Index on `status` for efficient querying of pending instructions.

---

## APIs

### Backend Server API (`main_server.py`)

#### 1. **Add New Task**

- **Endpoint**: `/add_task`
- **Method**: `POST`
- **Parameters**:
  - `task_description`: Description of the main task (JSON body).
- **Response**:
  - `task_id`: Unique identifier for the created task.
  - `instructions`: List of instruction IDs and their statuses.
- **Process**:
  - Receives the task description.
  - Uses the LLM to decompose the task into instructions.
  - Inserts the main task and instructions into MongoDB.
  - Returns the `task_id` and instructions information.

#### 2. **Generate Actions**

- **Endpoint**: `/generate_actions`
- **Method**: `POST`
- **Parameters**:
  - `instruction_id`: Identifier of the instruction (form data).
  - `screenshot`: Image file of the current screen (multipart/form-data).
- **Response**:
  - `instruction_id`: Identifier of the instruction.
  - `actions`: List of actions to perform.
- **Process**:
  - Validates and processes the input.
  - Retrieves the instruction and its `action_history` from MongoDB.
  - Calls the Vision System to detect GUI elements.
  - Uses the LLM Interface to determine the next actions.
  - Updates the `action_history` in MongoDB.
  - Returns the actions to the desktop application.

---

## Error Handling and Logging

- **Error Handling**:
  - Validates input data and files.
  - Handles exceptions during image processing, LLM communication, and database operations.
  - Returns appropriate HTTP status codes and error messages.
- **Logging**:
  - Logs significant events like errors, API calls, database operations, and action executions.
  - Stores logs for debugging and monitoring purposes.
- **Retry Mechanisms**:
  - Implements retries for transient errors, especially when communicating with external APIs like OpenAI or Google Vision.

---

## Security Considerations

- **API Security**:
  - Implements authentication and authorization for API endpoints.
  - Uses HTTPS to encrypt data in transit.
- **Data Protection**:
  - Sanitizes inputs to prevent injection attacks.
  - Stores sensitive data like API keys securely, using environment variables or secret managers.
- **Access Control**:
  - Restricts access to the MongoDB database.
- **Compliance**:
  - Ensures compliance with data protection regulations, especially when handling screenshots that may contain sensitive information.

---

## Scalability and Performance

- **Asynchronous Processing**:
  - Uses `asyncio` and `httpx` for non-blocking I/O operations.
- **Load Distribution**:
  - Deploys the backend server behind a load balancer for horizontal scaling.
- **Efficient Database Operations**:
  - Uses indexing and optimized queries for MongoDB to ensure efficient data retrieval.
- **Caching**:
  - Implements caching strategies for repeated tasks or common GUI elements.
- **Resource Optimization**:
  - Efficiently manages memory and CPU usage, especially when processing images and interacting with LLMs.

---

## Conclusion

Amyable aims to automate tasks by intelligently interpreting the current state of the desktop environment and determining the necessary actions to accomplish a given task. By combining computer vision, natural language processing, and automation tools, it provides a robust framework for task automation on a host machine. The updated design leverages MongoDB for task and instruction management, simplifying the architecture and enhancing scalability.

---

## Environment Variables

- `MONGODB_URI`: Connection string for MongoDB.
- `GOOGLE_CREDENTIALS_PATH`: Path to the Google Cloud credentials JSON file.
- `YOLO_MODEL_PATH`: Path to the YOLO model file.
- `OPENAI_API_KEY`: API key for accessing OpenAI services.

---

## Dependencies

- `fastapi`
- `uvicorn`
- `motor` (async MongoDB driver)
- `pydantic`
- `pyautogui`
- `google-cloud-vision`
- `ultralytics` (for YOLO)
- `Pillow`
- `httpx`
- `python-dotenv` (for environment variables)
- `asyncio`
- MongoDB

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/amyable.git
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Environment Variables**:
   - Create a `.env` file or set environment variables directly.
4. **Run the Backend Server**:
   ```bash
   uvicorn main_server:app --reload
   ```
5. **Run the Desktop Application**:
   - Execute the desktop app script or binary on the host machine.

---

## Testing

- **Unit Tests**:
  - Write tests for individual modules like Vision System, LLM Interface, Action Executor, and database operations.
- **Integration Tests**:
  - Test the end-to-end flow from task creation to action execution.
- **Performance Tests**:
  - Benchmark the response times of the backend server and action execution.

---

## Maintainers

- **Your Name**
- **Contact Information**
- **Project Repository Link**

---

*End of Document*

---
