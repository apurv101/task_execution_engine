# Amyable High-Level Design Document (Updated)

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
13. [Environment Variables](#environment-variables)
14. [Dependencies](#dependencies)
15. [Setup Instructions](#setup-instructions)
16. [Testing](#testing)
17. [Maintainers](#maintainers)

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

- **Function**: Submits new tasks, processes instructions by interacting with the backend server, and executes actions on the host machine.

- **Technologies**:
  - Python
  - `pyautogui` for automating GUI interactions
  - `requests` or `httpx` for HTTP communication with backend APIs

- **Responsibilities**:

  - **Task Submission**:
    - Call the `/add_task` API to submit a new task description.
    - Receive the `task_id` and list of instructions.
    - Store the `task_id` and instructions in memory.

  - **Instruction Processing**:
    - Loop over the instructions in the proper order.
    - For each instruction:
      - Capture the current screen state.
      - Call the `/generate_actions` API with the `instruction_id` and screenshot.
      - Execute the received actions using `pyautogui`.
      - Upon completion or failure, call the `/update_instruction_status` API to update the status of the instruction accordingly.

  - **Note**:
    - The desktop application no longer directly accesses the MongoDB database.
    - All interactions with tasks and instructions are done through the backend APIs.

### Backend Server

- **Function**: Processes incoming task descriptions and screenshots to generate the next actions, manages tasks and instructions in MongoDB, and handles instruction status updates.

- **Technologies**:
  - Python
  - FastAPI for building RESTful APIs
  - Google Vision API for text detection
  - YOLO model for object detection
  - OpenAI API for LLM integration
  - MongoDB for storing tasks, instructions, and action histories

- **Responsibilities**:
  - Receive task descriptions via the `/add_task` API and create tasks and instructions.
  - Use LLM to break down tasks into instructions.
  - Store tasks and instructions in MongoDB.
  - Receive `instruction_id` and screenshots from the desktop application via the `/generate_actions` API.
  - Use computer vision to interpret GUI elements.
  - Utilize LLM to determine the next actions.
  - Update action history in MongoDB.
  - Respond with the next actions to the desktop application.
  - Handle instruction status updates from the desktop application via the `/update_instruction_status` API.

### MongoDB Database

- **Function**: Stores tasks, instructions, and action histories for the application.

- **Technologies**:
  - MongoDB
  - `motor` (async MongoDB driver for Python)

- **Responsibilities**:
  - Store main tasks with their descriptions and list of instruction IDs.
  - Store instructions with their descriptions, statuses, and action histories.
  - Provide efficient querying mechanisms for tasks and instructions.
  - Ensure data consistency and integrity.

---

## Workflow

### Adding a New Task

1. **Task Submission**:

   - The desktop application calls the `/add_task` API with the task description.
   - The backend server receives the task description via the API.

2. **Task Decomposition**:

   - The backend server uses the LLM to generate instructions based on the main task description.

3. **Database Insertion**:

   - Inserts the main task into the `tasks` collection.
   - Inserts instructions into the `instructions` collection, referencing the `task_id`.

4. **Response to Desktop Application**:

   - The backend server returns the `task_id` and the list of instructions to the desktop application.

### Desktop Application Processing

1. **Instruction Processing**:

   - The desktop application stores the `task_id` and instructions in memory.
   - It loops over the instructions in the proper order.
   - For each instruction:

     a. **Action Generation**:

        - Captures the current screen state.
        - Calls the `/generate_actions` API with the `instruction_id` and screenshot.
        - Receives the next actions from the backend server.

     b. **Action Execution**:

        - Executes the received actions using `pyautogui`.

     c. **Instruction Status Update**:

        - Upon successful execution, calls the `/update_instruction_status` API to update the instruction status to "completed".
        - If execution fails, calls the `/update_instruction_status` API to update the instruction status to "failed".

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

6. **Instruction Status Update**:

   - Upon receiving a status update request from the desktop application via the `/update_instruction_status` API, the backend server updates the instruction status in the `tasks` and `instructions` collection accordingly.

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
- Enable retrieval and updating of tasks and instructions.

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
    }
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
  - `status`: Current status of the instruction (pending, in-progress, completed, failed).
  - `created_at`: Timestamp when the instruction was created.
  - `updated_at`: Timestamp when the instruction was last updated.

### Indexes

- **`tasks` Collection**:
  - Index on `task_id` (unique).
- **`instructions` Collection**:
  - Index on `instruction_id` (unique).
  - Index on `task_id` to enable efficient retrieval of instructions for a given task.
  - Index on `status` for efficient querying of instructions by status.

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
     - `instructions`: List of instruction IDs and their descriptions.
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

3. **Update Instruction Status**

   - **Endpoint**: `/update_instruction_status`
   - **Method**: POST
   - **Parameters**:
     - `instruction_id`: Identifier of the instruction (JSON body).
     - `status`: New status of the instruction ("completed" or "failed") (JSON body).
   - **Response**:
     - `instruction_id`: Identifier of the instruction.
     - `status`: Updated status.
     - `message`: Confirmation message.
   - **Process**:
     - Validates the `instruction_id` and `status`.
     - Updates the status of the instruction in the `tasks` collection.
     - Returns a confirmation message.

---

## Error Handling and Logging

- **Error Handling**:
  - Validates input data and files.
  - Handles exceptions during image processing, LLM communication, and database operations.
  - Returns appropriate HTTP status codes and error messages.
  - Specifically checks for valid `instruction_id` and `status` in `/update_instruction_status`.
- **Logging**:
  - Logs significant events like errors, API calls, database operations, and action executions.
  - Stores logs for debugging and monitoring purposes.
- **Retry Mechanisms**:
  - Implements retries for transient errors, especially when communicating with external APIs like OpenAI or Google Vision.
  - The desktop application should handle network errors when calling backend APIs and implement retries or failover strategies.

---

## Security Considerations

- **API Security**:
  - Implements authentication and authorization for API endpoints, including `/update_instruction_status`.
  - Uses HTTPS to encrypt data in transit.
- **Data Protection**:
  - Sanitizes inputs to prevent injection attacks.
  - Stores sensitive data like API keys securely, using environment variables or secret managers.
- **Access Control**:
  - Restricts access to the MongoDB database.
  - Ensures that only authorized desktop applications can update instruction statuses.
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

Amyable aims to automate tasks by intelligently interpreting the current state of the desktop environment and determining the necessary actions to accomplish a given task. By combining computer vision, natural language processing, and automation tools, it provides a robust framework for task automation on a host machine. The updated design removes direct database access from the desktop application, enhancing security, maintainability, and scalability by centralizing data interactions through backend APIs.

---

## Environment Variables

- `MONGODB_URI`: Connection string for MongoDB.
- `GOOGLE_CREDENTIALS_PATH`: Path to the Google Cloud credentials JSON file.
- `YOLO_MODEL_PATH`: Path to the YOLO model file.
- `OPENAI_API_KEY`: API key for accessing OpenAI services.
- `API_AUTH_TOKEN`: Token for authenticating API requests from the desktop application.

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
- `requests` (for HTTP communication)
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
  - Test the end-to-end flow from task creation to action execution, including API interactions.
- **Performance Tests**:
  - Benchmark the response times of the backend server and action execution.
- **Security Tests**:
  - Verify that unauthorized requests to the APIs are properly rejected.

---

## Maintainers

- **Your Name**
- **Contact Information**
- **Project Repository Link**

---

**End of Document**

---
