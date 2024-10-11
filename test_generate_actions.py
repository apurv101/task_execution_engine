# test_generate_actions.py

import requests
import os

def test_generate_actions(api_url, image_path, task_description, task_id=None):
    """
    Sends a POST request to the /generate_actions API endpoint with the given parameters.

    :param api_url: The URL of the API endpoint (e.g., http://localhost:8000/generate_actions)
    :param image_path: Path to the image file to upload
    :param task_description: Description of the task
    :param task_id: Optional task ID
    :return: Response from the API
    """
    # Check if the image file exists
    if not os.path.isfile(image_path):
        print(f"Error: Image file '{image_path}' does not exist.")
        return

    # Open the image file in binary mode
    with open(image_path, 'rb') as image_file:
        # Prepare the files and data payload
        files = {
            'screenshot': (os.path.basename(image_path), image_file, 'image/png')
        }

        # Prepare form data
        data = {
            'task_description': task_description
        }

        if task_id:
            data['task_id'] = task_id

        try:
            # Send the POST request
            response = requests.post(api_url, files=files, data=data, timeout=1000)

            # Raise an exception if the request was unsuccessful
            response.raise_for_status()

            # Parse the JSON response
            json_response = response.json()

            print("API Response:")
            print(json_response)

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            print(f"Response content: {response.text}")
        except Exception as err:
            print(f"An error occurred: {err}")

if __name__ == "__main__":
    # Configuration
    API_URL = "http://localhost:8000/generate_actions"  # Update if different
    IMAGE_PATH = "sample_screenshot.png"  # Path to your test image
    TASK_DESCRIPTION = "Create a new customer named Acme Corporation"
    TASK_ID = None  # Replace with an existing task ID to test updating, or leave as None for a new task

    # Run the test
    test_generate_actions(API_URL, IMAGE_PATH, TASK_DESCRIPTION, TASK_ID)