
# Aimyable Task Execution Engine

## Overview

The Aimyable Task Execution Engine is a part of an AI-powered automation system designed to handle tasks typically performed by accounting clerks. This system aims to automate GUI interactions across various environments (such as Outlook and QuickBooks) by detecting screen elements and performing actions like mouse movements, clicks, typing, and more. It employs LLMs (Large Language Models) to dynamically determine the next action required for task completion based on screen elements and task history.

The system comprises several components:

- **Action Executor**: Executes GUI actions like moving the mouse, clicking, typing, scrolling, dragging, and more using `pyautogui`.
- **LLM Interface**: Interacts with LLMs (e.g., GPT) to generate prompts and predict the next required action.
- **Vision System**: Detects GUI elements on the screen using the Google Vision API for text elements and YOLO for object detection.
- **Test Action Interface**: This is used to validate and test the interaction between action prediction, vision detection, and execution.

### Key Features

1. **Automating GUI Tasks**: The system focuses on automating repetitive tasks like interacting with GUI elements in software like QuickBooks and Outlook.
2. **Screen Element Detection**: It uses a combination of Google Vision OCR and YOLO object detection to identify text and GUI elements, such as buttons, input fields, and icons, from screenshots.
3. **LLM-Driven Task Execution**: By feeding the detected elements and task history into an LLM, the system can predict and execute the next action (e.g., moving the mouse, clicking, typing).
4. **High-Level to Low-Level Task Translation**: The system translates high-level tasks into detailed, low-level actions, such as mouse movements and keyboard inputs, which are performed on the screen.
5. **Cross-Environment Automation**: Aimyable can interact with various software environments like Outlook and QuickBooks by analyzing the screen, detecting elements, and taking actions dynamically.

## System Components

### 1. **Action Executor (`action_executor.py`)**

The Action Executor handles the actual GUI automation by performing actions such as:
- Moving the mouse to specific coordinates.
- Clicking, double-clicking, and right-clicking.
- Typing text into input fields.
- Pressing keys or key combinations.
- Dragging items from one location to another.
- Scrolling by a specific amount.

It scales the detected element coordinates from the screenshot to match the actual screen resolution to ensure precise actions.

### 2. **LLM Interface (`llm_interface.py`)**

The LLM Interface generates prompts to guide the next action the system should take. It sends the prompt to an LLM (like GPT-4) and parses the response to determine the next GUI action. The prompts include:
- Task description.
- Detected text elements (via Google Vision).
- Detected GUI elements (via YOLO).
- Action history (the steps that have already been performed).

The LLM predicts the next action in JSON format, which is parsed and executed by the Action Executor.

### 3. **Vision System (`vision_system.py`)**

The Vision System takes a screenshot of the current state of the GUI and uses:
- **Google Vision API** for text detection.
- **YOLO model** for object detection (e.g., icons, buttons).

It returns a list of detected GUI elements, including their bounding boxes and additional metadata like confidence scores.

### 4. **Test Action Interface (`test_action_interface.py`)**

This module tests the interaction between the LLM interface, vision system, and action executor by:
- Sending a task to the LLM for action prediction.
- Detecting GUI elements using the vision system.
- Executing the predicted actions via the Action Executor.

## Workflow

1. **Capture the Current Screen**: The system captures a screenshot of the current state of the desktop.
2. **Detect GUI Elements**: The screenshot is processed to detect text elements (using Google Vision) and GUI elements (using YOLO).
3. **Generate Action Prompt**: The detected elements and action history are sent to the LLM as a prompt to predict the next action.
4. **Predict the Next Action**: The LLM suggests the next action in JSON format, specifying the type of action (e.g., `moveTo`, `click`, `type`) and relevant elements on the screen.
5. **Execute the Action**: The Action Executor performs the predicted action, such as moving the mouse to a specific location, clicking, or typing.
6. **Repeat Until Task Completion**: The process continues until the task is marked as finished.

## Use Case

The Aimyable Task Execution Engine is primarily designed to automate tasks in environments like QuickBooks and Outlook, handling clerical tasks such as:
- Reading emails.
- Creating and verifying invoices.
- Entering data into accounting software.

The system can dynamically adjust its actions based on the current state of the screen, making it flexible enough to handle a wide variety of tasks without hardcoding specific steps.

## Installation

To set up the system, you need to install the following dependencies:

- `pyautogui`: For GUI automation (mouse movement, clicking, typing, etc.).
- `Pillow`: To handle images (screenshots).
- `google-cloud-vision`: For Google Vision API to detect text elements.
- `ultralytics`: For YOLO object detection model.
- `requests`: To interact with the LLM API.
- `python-dotenv`: To load environment variables

Run the following command to install these dependencies:

```bash
pip install pyautogui Pillow google-cloud-vision ultralytics requests python-dotenv
```

You will also need to set up Google Vision API credentials for text detection. Follow the [Google Cloud documentation](https://cloud.google.com/vision/docs/setup) for instructions.

## Configuration

1. **Google Vision API**: Set the path to your Google Cloud credentials in the environment variable `GOOGLE_APPLICATION_CREDENTIALS`.
2. **YOLO Model**: Provide the path to the YOLO model file (e.g., `.pt` file) for object detection.
3. **LLM API Key**: Add your LLM API key for interacting with the GPT-based model to predict the next action.

```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/google_credentials.json"
```

## Future Plans

The next steps for Aimyable include:
- Enhancing the LLM prompts to handle more complex tasks.
- Expanding the Vision System to work with more advanced object detection models.
- Improving task prediction by incorporating additional task history and contextual data.

