# mock_llm_interface.py

import io
from typing import Optional
import json
from PIL import Image

def generate_action_clickable_prompt(task_description, google_vision_elements, yolo_elements, action_history):
    # Mocked prompt generation - can be empty or return a fixed string
    return "This is a mocked prompt for testing purposes."

class LLMInterface:
    def __init__(self, api_key):
        self.api_key = api_key
        # Mock initialization
        print("Initialized MockLLMInterface with API key (mocked).")

    async def decompose_task(self, task_description):
        """
        Mocks the task decomposition by returning a static list of instructions.
        """
        # Mock decomposition based on the task_description
        print(f"Mock decomposing task: {task_description}")

        # Return a fixed set of instructions for testing
        return [
            "Open the web browser",
            "Navigate to google.com",
            "Search for 'Python programming'",
            "Open the first search result"
        ]

    async def generate_next_action(
        self,
        task: str,
        google_vision_elements: list,
        yolo_elements: list,
        action_history: list,
        image: Optional[Image.Image] = None
    ):
        """
        Mocks the next action generation by returning static actions.
        """
        print("Mock generating next action...")

        # Return a fixed set of actions
        action = {
            "actions": [
                {
                    "action": "moveTo",
                    "text_elements": [],
                    "gui_elements": [],
                    "clickable_coordinates": [500, 300],
                    "description": "Mock action: Move mouse to coordinates (500, 300)"
                },
                {
                    "action": "click",
                    "text_elements": [],
                    "gui_elements": [],
                    "clickable_coordinates": [500, 300],
                    "description": "Mock action: Click at coordinates (500, 300)"
                }
            ]
        }
        return action

    def update_plan(self, plan, action_history):
        """
        Optionally updates the plan based on the action history.
        Currently returns the original plan.
        """
        # Mock plan updating logic
        print("Mock updating plan based on action history.")
        return plan

    def _parse_action_from_response(self, response_text):
        """
        Parses the JSON action from the LLM response.
        """
        # Since we're mocking, we won't parse any response
        print("Mock parsing action from response (not needed).")
        pass  # Placeholder