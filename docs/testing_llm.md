
# LLM Interface Testing Guide

This guide will help you set up and test the `llm_interface` module of the system. It includes instructions on setting up the environment from scratch, configuring the vision system (Google Vision API and YOLO model), and running the test script with sample screenshots.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
  - [3. Install Required Packages](#3-install-required-packages)
- [Setting Up the Vision System](#setting-up-the-vision-system)
  - [1. Google Vision API](#1-google-vision-api)
    - [a. Create a Google Cloud Project](#a-create-a-google-cloud-project)
    - [b. Enable the Vision API](#b-enable-the-vision-api)
    - [c. Set Up Authentication](#c-set-up-authentication)
  - [2. YOLO Model](#2-yolo-model)
    - [a. Install Ultralytics YOLOv8](#a-install-ultralytics-yolov8)
    - [b. Download or Train a YOLOv8 Model](#b-download-or-train-a-yolov8-model)
- [Setting Up the LLM Interface](#setting-up-the-llm-interface)
  - [1. Obtain OpenAI API Key](#1-obtain-openai-api-key)
- [Running the Test Script](#running-the-test-script)
  - [1. Prepare Test Images](#1-prepare-test-images)
  - [2. Update the Test Script](#2-update-the-test-script)
  - [3. Run the Test Script](#3-run-the-test-script)
- [Understanding the Test Script](#understanding-the-test-script)
- [Notes and Troubleshooting](#notes-and-troubleshooting)

## Overview

The `llm_interface` module interacts with a Large Language Model (LLM) to generate the next action based on the task description, current GUI elements detected from screenshots, and action history. The vision system uses Google Vision API and a YOLO model to detect text and GUI elements in screenshots.

This guide will walk you through setting up the necessary components and running a test script to validate the `llm_interface`.

## Prerequisites

- Python 3.7 or higher
- An OpenAI API key (for LLM interaction)
- A Google Cloud account (for Vision API)
- Basic knowledge of Python and virtual environments

## Environment Setup

### 1. Clone the Repository

First, clone the repository containing the project code.

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

*Replace `https://github.com/yourusername/yourrepository.git` with the actual repository URL.*

### 2. Create a Virtual Environment

Create a virtual environment to manage dependencies.

```bash
python3 -m venv venv
```

Activate the virtual environment:

- On Unix or MacOS:

  ```bash
  source venv/bin/activate
  ```

- On Windows:

  ```bash
  venv\Scripts\activate
  ```

### 3. Install Required Packages

Install the necessary Python packages using `pip`.

```bash
pip install -r requirements.txt
```

*Ensure that `requirements.txt` includes all necessary packages. If it doesn't exist, you can install packages individually as listed below.*

Alternatively, install the required packages manually:

```bash
pip install openai
pip install pyautogui
pip install google-cloud-vision
pip install ultralytics
pip install pillow
pip install opencv-python
pip install numpy
```

## Setting Up the Vision System

### 1. Google Vision API

#### a. Create a Google Cloud Project

- Go to the [Google Cloud Console](https://console.cloud.google.com/).
- Create a new project or select an existing one.

#### b. Enable the Vision API

- In the Cloud Console, navigate to **APIs & Services > Library**.
- Search for **Vision API** and click on it.
- Click **Enable** to enable the API for your project.

#### c. Set Up Authentication

- Navigate to **APIs & Services > Credentials**.
- Click **Create credentials** and select **Service account**.
- Fill in the necessary details and create a **JSON key**.
- Download the JSON key file and save it securely.

*For this guide, we'll assume you've saved it at `/path/to/your/credentials.json`.*

- Set the environment variable `GOOGLE_APPLICATION_CREDENTIALS` to point to your JSON key file:

  ```bash
  export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
  ```

  *On Windows:*

  ```cmd
  set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\credentials.json"
  ```

### 2. YOLO Model

#### a. Install Ultralytics YOLOv8

We will use the Ultralytics YOLOv8 model for object detection.

```bash
pip install ultralytics
```

#### b. Download or Train a YOLOv8 Model

You can either:

- **Download a Pretrained Model:**

  Download a pretrained YOLOv8 model suitable for your task.

- **Train Your Own Model:**

  If you have a custom dataset of GUI elements, you can train your own YOLOv8 model.

*For this guide, we'll assume you've saved the model at `/path/to/your/yolov8_model.pt`.*

## Setting Up the LLM Interface

### 1. Obtain OpenAI API Key

- Sign up or log in to your [OpenAI account](https://platform.openai.com/).
- Go to **API Keys** under your account settings.
- Generate a new API key.

*Keep your API key secure and do not share it publicly.*

Set the environment variable `OPENAI_API_KEY`:

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

*On Windows:*

```cmd
set OPENAI_API_KEY="your-openai-api-key"
```

## Running the Test Script

### 1. Prepare Test Images

Ensure you have the test screenshots available. For this guide, we'll assume you have three screenshots:

- `/path/to/your/screenshots/test_image_1.png`
- `/path/to/your/screenshots/test_image_2.png`
- `/path/to/your/screenshots/test_image_3.png`

Update the paths in the test script accordingly.

### 2. Update the Test Script

Create or update the test script `test_llm_interface.py` with the following content:

```python
import os
from llm_interface import LLMInterface
from vision_system import VisionSystem

# Task description
task = "Create a new customer named Acme Corporation"

# Paths to test images
test_image_1 = "/path/to/your/screenshots/test_image_1.png"
test_image_2 = "/path/to/your/screenshots/test_image_2.png"
test_image_3 = "/path/to/your/screenshots/test_image_3.png"

# Paths to credentials and model
google_credentials_path = "/path/to/your/credentials.json"
yolo_model_path = "/path/to/your/yolov8_model.pt"

# Initialize history
history = []

# Initialize interfaces
llm_interface = LLMInterface(api_key=os.getenv("OPENAI_API_KEY"))
vision_system = VisionSystem(google_credentials_path, yolo_model_path)

# Generate GUI elements for the first image
google_vision_elements = vision_system.detect_text(test_image_1)
yolo_elements = vision_system.yolo_service(test_image_1)

# Generate the first action
action1 = llm_interface.generate_next_action(
    task,
    google_vision_elements,
    yolo_elements,
    history,
    test_image_1
)

print("Action 1:", action1)

# Update history
history.extend(action1.get('actions', []))

# Repeat for subsequent images as needed
# For example, generate action for the second image
google_vision_elements = vision_system.detect_text(test_image_2)
yolo_elements = vision_system.yolo_service(test_image_2)

action2 = llm_interface.generate_next_action(
    task,
    google_vision_elements,
    yolo_elements,
    history,
    test_image_2
)

print("Action 2:", action2)

# Update history
history.extend(action2.get('actions', []))

# And so on for the third image
google_vision_elements = vision_system.detect_text(test_image_3)
yolo_elements = vision_system.yolo_service(test_image_3)

action3 = llm_interface.generate_next_action(
    task,
    google_vision_elements,
    yolo_elements,
    history,
    test_image_3
)

print("Action 3:", action3)
```

**Notes:**

- Replace `/path/to/your/credentials.json` with the actual path to your Google credentials JSON file.
- Replace `/path/to/your/yolov8_model.pt` with the actual path to your YOLO model.
- Replace the test image paths with the actual paths to your test images.

### 3. Run the Test Script

Ensure your virtual environment is activated and run:

```bash
python test_llm_interface.py
```

You should see the actions generated by the LLM printed to the console.

## Understanding the Test Script

The test script performs the following steps:

1. **Initialize the Task and Interfaces:**

   - Defines the task: "Create a new customer named Acme Corporation".
   - Initializes the `LLMInterface` and `VisionSystem` with the necessary credentials and models.

2. **Process Each Test Image:**

   - For each test image:
     - Uses the vision system to detect text elements (Google Vision API) and GUI elements (YOLO model).
     - Calls `llm_interface.generate_next_action()` to generate the next action based on the task, GUI elements, action history, and the current screenshot.
     - Prints the generated action.
     - Updates the action history.

3. **Repeat for Additional Images:**

   - You can process multiple images in sequence to simulate the step-by-step progression of the task.

## Notes and Troubleshooting

- **Environment Variables:**

  Ensure that `OPENAI_API_KEY` and `GOOGLE_APPLICATION_CREDENTIALS` environment variables are set correctly.

- **Google Vision API Quotas:**

  Be aware of the quotas and limits associated with the Google Vision API. Exceeding these may result in errors.

- **OpenAI API Usage:**

  Keep track of your OpenAI API usage to avoid unexpected charges.

- **Error Handling:**

  The script provided is a basic example. In a production environment, you should include error handling for API calls, file I/O, and other operations.

- **Debugging:**

  If you encounter issues, you can add print statements or use a debugger to inspect variables at different stages.

- **Dependencies:**

  Ensure all dependencies are installed and compatible with your Python version.

- **Version Compatibility:**

  Some packages may have compatibility issues with certain Python versions. It's recommended to use Python 3.8 or higher.

- **Custom Models:**

  If you train a custom YOLO model, ensure it's trained to recognize the GUI elements relevant to your application.

- **Privacy and Security:**

  Do not commit your API keys or credentials to version control. Use environment variables or secure credential management systems.

## Conclusion

By following this guide, you should be able to set up the environment, configure the vision system, and run the test script to validate the `llm_interface`. This setup forms the foundation for automating tasks based on high-level descriptions and can be expanded upon for more complex scenarios.

Happy testing!

