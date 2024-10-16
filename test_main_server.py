# test_main_server.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime, timezone

from main_server import app

# --------------------
# Mock Data for Testing
# --------------------

mock_task_description = "Automate sending an email."
mock_instruction_list = [
    "Open the email client.",
    "Compose a new email.",
    "Enter the recipient's address.",
    "Write the subject and body.",
    "Send the email."
]
mock_instruction_id = "mock-instruction-id"
mock_task_id = "mock-task-id"

mock_action_response = {
    "actions": ["Click on 'New Email' button", "Type in the recipient's email address"]
}

mock_vision_elements = {
    "text_elements": ["File", "Edit", "View", "Help"],
    "object_elements": ["button", "text_field"]
}

# Mock image data
mock_image_data = b"fake-image-data"

# --------------------
# Fixtures
# --------------------

@pytest.fixture
def mock_datetime(monkeypatch):
    """
    Fixture to mock datetime.now(timezone.utc) to return a fixed datetime.
    """
    fixed_datetime = datetime(2021, 1, 1, tzinfo=timezone.utc)

    class MockDateTime:
        @classmethod
        def now(cls, tz=None):
            return fixed_datetime

    # Patch 'datetime' in 'main_server.py' with MockDateTime
    monkeypatch.setattr('main_server.datetime', MockDateTime)

@pytest.fixture
def mock_helpers(monkeypatch):
    """
    Fixture to mock helper functions and external dependencies.
    Sets up mocks for database operations, external service calls, and image processing.
    Also mocks 'app.db', 'app.llm_interface', and 'app.vision_system'.
    """
    with patch('main_server.decompose_task') as mock_decompose_task, \
         patch('main_server.insert_instructions') as mock_insert_instructions, \
         patch('main_server.insert_task') as mock_insert_task, \
         patch('main_server.find_instruction') as mock_find_instruction, \
         patch('main_server.process_image') as mock_process_image, \
         patch('main_server.generate_next_action') as mock_generate_next_action, \
         patch('main_server.update_instruction_action_history') as mock_update_instruction_action_history, \
         patch('main_server.Image.open') as mock_image_open, \
         patch('main_server.AsyncIOMotorClient') as mock_mongo_client:

        # Mock 'decompose_task' to return a predefined list of instructions
        mock_decompose_task.return_value = mock_instruction_list

        # Mock database insertion functions
        mock_insert_instructions.return_value = AsyncMock()
        mock_insert_task.return_value = AsyncMock()

        # Mock 'find_instruction' to return a predefined instruction document
        mock_find_instruction.return_value = {
            "instruction_id": mock_instruction_id,
            "task_id": mock_task_id,
            "instruction_description": mock_instruction_list[0],
            "action_history": [],
            "status": "pending",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }

        # Mock 'process_image' to return predefined vision elements
        mock_process_image.return_value = (mock_vision_elements['text_elements'], mock_vision_elements['object_elements'])

        # Mock 'generate_next_action' to return a predefined action response
        mock_generate_next_action.return_value = mock_action_response

        # Mock 'update_instruction_action_history' to simulate database update
        mock_update_instruction_action_history.return_value = AsyncMock()

        # Mock 'Image.open' to prevent actual I/O operations
        mock_image = MagicMock()
        mock_image.convert.return_value = mock_image
        mock_image_open.return_value = mock_image

        # Mock MongoDB client and database
        mock_db = MagicMock()
        mock_client_instance = mock_mongo_client.return_value
        mock_client_instance.__getitem__.return_value = mock_db

        # Assign the mock database to 'app.db'
        app.db = mock_db

        # Additionally, mock 'app.llm_interface' and 'app.vision_system'
        app.llm_interface = MagicMock()
        app.vision_system = MagicMock()

        yield {
            "mock_decompose_task": mock_decompose_task,
            "mock_insert_instructions": mock_insert_instructions,
            "mock_insert_task": mock_insert_task,
            "mock_find_instruction": mock_find_instruction,
            "mock_process_image": mock_process_image,
            "mock_generate_next_action": mock_generate_next_action,
            "mock_update_instruction_action_history": mock_update_instruction_action_history,
            "mock_image_open": mock_image_open,
            "mock_db": mock_db
        }

@pytest.fixture
def client_fixture(mock_helpers, mock_datetime):
    """
    Fixture to create a TestClient instance after all mocks are in place.
    Ensures that 'app.llm_interface' and 'app.vision_system' are already mocked before TestClient is instantiated.
    """
    with TestClient(app) as client:
        yield client

# --------------------
# Tests
# --------------------

def test_add_task(client_fixture, mock_helpers, mock_datetime):
    """
    Test the /add_task endpoint to ensure a new task is added correctly.
    """
    response = client_fixture.post(
        "/add_task",
        json={"task_description": mock_task_description}
    )

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Parse the response JSON
    response_json = response.json()
    assert 'task_id' in response_json, "Response JSON does not contain 'task_id'"
    assert 'instructions' in response_json, "Response JSON does not contain 'instructions'"

    # Verify that the helper functions were called
    assert mock_helpers['mock_decompose_task'].called, "decompose_task was not called"
    assert mock_helpers['mock_insert_instructions'].called, "insert_instructions was not called"
    assert mock_helpers['mock_insert_task'].called, "insert_task was not called"

def test_generate_actions(client_fixture, mock_helpers, mock_datetime):
    """
    Test the /generate_actions endpoint to ensure actions are generated correctly.
    """
    # Prepare the files and data for the request
    files = {
        "screenshot": ("screenshot.png", mock_image_data, "image/png")
    }
    data = {
        "instruction_id": mock_instruction_id
    }

    response = client_fixture.post(
        "/generate_actions",
        files=files,
        data=data
    )

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Parse the response JSON
    response_json = response.json()
    assert 'instruction_id' in response_json, "Response JSON does not contain 'instruction_id'"
    assert 'actions' in response_json, "Response JSON does not contain 'actions'"
    assert response_json['instruction_id'] == mock_instruction_id, f"Expected instruction_id '{mock_instruction_id}', got '{response_json['instruction_id']}'"
    assert response_json['actions'] == mock_action_response['actions'], "Actions in response do not match expected actions"

    # Verify that the helper functions were called
    assert mock_helpers['mock_find_instruction'].called, "find_instruction was not called"
    assert mock_helpers['mock_process_image'].called, "process_image was not called"
    assert mock_helpers['mock_generate_next_action'].called, "generate_next_action was not called"
    assert mock_helpers['mock_update_instruction_action_history'].called, "update_instruction_action_history was not called"