# desktop_application.py

import requests
import pyautogui
import io
import time
import json
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base URL of the backend server
BASE_URL = 'http://localhost:8000'

def create_task(task_description):
    """
    Sends a POST request to create a new task.
    """
    url = f'{BASE_URL}/add_task'
    data = {'task_description': task_description}
    try:
        logging.info(f"Creating task with description: '{task_description}'")
        response = requests.post(url, json=data)
        response.raise_for_status()
        task = response.json()
        logging.info(f"Task created with ID: {task.get('task_id')}")
        return task
    except requests.exceptions.RequestException as e:
        logging.error(f"Error creating task: {e}")
        return None

def generate_actions(instruction_id, image_bytes):
    """
    Sends a POST request to generate actions for a given instruction.
    """
    url = f'{BASE_URL}/generate_actions'
    files = {
        'screenshot': ('screenshot.png', image_bytes, 'image/png')
    }
    data = {'instruction_id': instruction_id}
    try:
        logging.info(f"Generating actions for Instruction ID: {instruction_id}")
        response = requests.post(url, data=data, files=files)
        response.raise_for_status()
        actions_response = response.json()
        logging.debug(f"Actions received: {actions_response}")
        return actions_response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error generating actions for instruction {instruction_id}: {e}")
        return None

def update_instruction_status(instruction_id, status):
    """
    Sends a POST request to update the status of an instruction.
    """
    url = f'{BASE_URL}/update_instruction_status'
    data = {
        'instruction_id': instruction_id,
        'status': status
    }
    try:
        logging.info(f"Updating Instruction ID: {instruction_id} to status: '{status}'")
        response = requests.post(url, json=data)
        response.raise_for_status()
        update_response = response.json()
        logging.info(f"Instruction {instruction_id} status updated to '{status}'")
        return update_response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error updating status for instruction {instruction_id}: {e}")
        return None

def execute_action(actions):
    """
    Mock function to execute actions.
    Replace this with the actual implementation.
    """
    logging.info("Executing actions:")
    for action in actions:
        logging.info(f" - {action}")
        # Here you would implement the actual action execution using pyautogui or other tools
        # For demonstration, we'll just sleep for a short duration
        time.sleep(0.5)
    # Simulate a successful execution
    return True

def capture_screenshot():
    """
    Captures the current screen and returns the image bytes.
    """
    try:
        screenshot = pyautogui.screenshot()
        img_byte_arr = io.BytesIO()
        screenshot.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    except Exception as e:
        logging.error(f"Error capturing screenshot: {e}")
        return None

def process_instruction(instruction):
    """
    Processes a single instruction by generating actions until 'finish' is received,
    executing the actions, and updating the instruction status.
    """
    instruction_id = instruction.get('instruction_id')
    instruction_description = instruction.get('instruction_description', 'No description provided.')
    logging.info(f"\nProcessing Instruction: {instruction_description} (ID: {instruction_id})")

    finish_received = False

    while not finish_received:
        # Capture screenshot
        screenshot_bytes = capture_screenshot()
        if not screenshot_bytes:
            logging.error("Failed to capture screenshot. Marking instruction as failed.")
            update_instruction_status(instruction_id, "failed")
            return

        # Generate actions
        actions_response = generate_actions(instruction_id, screenshot_bytes)
        if not actions_response:
            logging.error("Failed to generate actions. Marking instruction as failed.")
            update_instruction_status(instruction_id, "failed")
            return

        actions = actions_response.get('actions', [])
        if not actions:
            logging.warning("No actions received. Continuing to next iteration.")
            time.sleep(1)
            continue

        logging.info(f"Actions received: {actions}")

        # Execute received actions
        success = execute_action(actions)
        if not success:
            logging.error("Action execution failed. Marking instruction as failed.")
            update_instruction_status(instruction_id, "failed")
            return

        # Check for 'finish' action
        for action in actions:
            if action.get('type') == 'finish':
                finish_received = True
                logging.info("Received 'finish' action.")
                break

        # Optional: Add a delay to prevent rapid API calls
        time.sleep(1)

    # Update instruction status
    update_instruction_status(instruction_id, "completed")

def main():
    # Step 1: Create a new task
    task_description = "Open a web browser and navigate to google.com"
    task_response = create_task(task_description)
    if not task_response:
        logging.error("Task creation failed. Exiting.")
        return

    print("\nTask created:")
    print(json.dumps(task_response, indent=2, default=str))

    instructions = task_response.get('instructions', [])
    if not instructions:
        logging.error("No instructions found. Exiting.")
        return

    # Step 2: Process each instruction
    for instruction in instructions:
        process_instruction(instruction)

if __name__ == '__main__':
    main()