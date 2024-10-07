import requests
import json
import base64




def generate_action_clickable_prompt(task_description, google_vision_elements, yolo_elements, action_history):
    return f"""
I need to perform the task: '{task_description}'.
I have just taken a screenshot of the current state of the screen. Look at the screenshot to understand what software we are using and where we are in the process.

I have two lists of GUI elements extracted from the current screen:

1. **Text Elements** detected by Google Vision OCR (each element is a dictionary with keys 'element', 'bounding_box', 'text', 'type'):
{google_vision_elements}

2. **GUI Elements** detected by the YOLO object detection model (each element is a dictionary with keys 'element', 'bounding_box', 'confidence', 'type'):
{yolo_elements}

The action history (the actions already performed) is:
{action_history}

Based on this information, predict the next action I need to perform to accomplish the task.

The next action must correspond to one of the following types:
- Move the mouse to a specific position (e.g., **moveTo** action).
- Click at a specific position (e.g., **click** action).
- Double-click at a specific position (e.g., **doubleClick** action).
- Right-click at a specific position (e.g., **rightClick** action).
- Scroll by a specific amount (e.g., **scroll** action).
- Type text into a specific input field (e.g., **type** action).
- Press specific keyboard keys (e.g., **press** action).
- Drag from one position to another (e.g., **drag** action).
- Finish the task (e.g., **finish** action).

When suggesting the next action, please specify:
1. The type of action.
2. The relevant **Text Elements** from the Google Vision OCR output that are associated with the action (as a list of dicts).
3. The relevant **GUI Elements** from the YOLO output that are associated with the action (as a list of dicts).
4. The final clickable coordinates where the action should be performed (as a tuple [x, y]).
5. Provide a brief description of the action.
6. If the action involves typing or key presses, provide the exact text or key combination.

Other things to keep in mind:
- Instead of using icons on dashboard, we will always prefer using the side menu or the top menu.
- We will need to move the mouse to a specific location first before clicking.
- When determining the relevant GUI elements, find YOLO elements that are close to or overlap with the relevant text elements.
- Only suggest those actions that can be inferred from the current screen. Do not suggest actions that require additional information.


The output should be in valid JSON format so it can be parsed programmatically. For example:
```json
{{
    "actions": [
        {{
            "action": "moveTo",
            "text_elements": [
                {{"element": "Outlook Icon", "bounding_box": [100, 100, 150, 150], "text": "Outlook", "type": "text"}}
            ],
            "gui_elements": [
                {{"element": "icon", "bounding_box": [90, 90, 160, 160], "confidence": 0.95, "type": "object"}}
            ],
            "clickable_coordinates": [125, 125],
            "description": "Move mouse to the Outlook icon to open Outlook"
        }},
        {{
            "action": "doubleClick",
            "text_elements": [
                {{"element": "Outlook Icon", "bounding_box": [100, 100, 150, 150], "text": "Outlook", "type": "text"}}
            ],
            "gui_elements": [
                {{"element": "icon", "bounding_box": [90, 90, 160, 160], "confidence": 0.95, "type": "object"}}
            ],
            "clickable_coordinates": [125, 125],
            "description": "Double-click on the Outlook icon to open the application"
        }}
    ]
}}

"""




class LLMInterface:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = { "Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}" } 
        # Define the API URL here 
        self.api_url = "https://api.openai.com/v1/chat/completions"
        # Initialize LLM client here, e.g., OpenAI GPT
        # Placeholder for actual implementation


    def generate_next_action(self, task, google_vision_elements, yolo_elements, action_history, image_path=None):
        """
        Generates the next action to perform based on the current plan,
        GUI elements, action history, and an optional image (screenshot).
        """
        print("Generating next action...")
        # change here
        prompt = generate_action_clickable_prompt(task, google_vision_elements, yolo_elements, action_history)
        ## append the prompt to file
        with open("prompt_test.txt", "a", encoding="utf-8") as f:
            f.write(prompt)
            f.write("#"*100)
            f.write("\n\n")

        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "max_tokens": 4096
        }

        if image_path:
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            image_url_content = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            }
            payload['messages'][0]['content'].append(image_url_content)

        response = requests.post(self.api_url, headers=self.headers, json=payload)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None

        completion = response.json()
        action_text = completion['choices'][0]['message']['content']

        # Parse the JSON action from the response
        action = self._parse_action_from_response(action_text)
        return action


    def update_plan(self, plan, action_history):
        """
        Optionally updates the plan based on the action history.
        Currently returns the original plan.
        """
        # Placeholder for plan updating logic
        return plan
    

    def _parse_action_from_response(self, response_text):
        """
        Parses the JSON action from the LLM response.
        """
        try:
            # Find the JSON block in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            json_str = response_text[json_start:json_end]

            # Load the JSON data
            action = json.loads(json_str)
            return action
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print("LLM Response:", response_text)
            return None
