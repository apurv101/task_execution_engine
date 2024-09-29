import time
import json
import os
# Import the necessary modules
from llm_interface import LLMInterface
from vision_system import VisionSystem
from action_executor import ActionExecutor
from action_history import ActionHistory
from PIL import Image


action1 = {
    "actions": [
        {
            "action": "moveTo",
            "text_elements": [
                {
                    "element": "Customers",
                    "bounding_box": [
                        72,
                        1080,
                        210,
                        1100
                    ],
                    "text": "Customers",
                    "type": "text"
                },
                {
                    "element": "&",
                    "bounding_box": [
                        218,
                        1080,
                        236,
                        1100
                    ],
                    "text": "&",
                    "type": "text"
                },
                {
                    "element": "leads",
                    "bounding_box": [
                        245,
                        1080,
                        314,
                        1100
                    ],
                    "text": "leads",
                    "type": "text"
                }
            ],
            "gui_elements": [
                {
                    "element": "button",
                    "bounding_box": [
                        2.2720413,
                        1606.9541,
                        438.0704,
                        1703.7102
                    ],
                    "confidence": 0.7675509,
                    "type": "object"
                },
                {
                    "element": "button",
                    "bounding_box": [
                        2.295353,
                        1710.0834,
                        441.2123,
                        1799.217
                    ],
                    "confidence": 0.81576186,
                    "type": "object"
                }
            ],
            "clickable_coordinates": [
                73,
                1090
            ],
            "description": "Move mouse to the 'Customers' menu item to open the customer section"
        },
        {
            "action": "click",
            "text_elements": [
                {
                    "element": "Customers",
                    "bounding_box": [
                        72,
                        1080,
                        210,
                        1100
                    ],
                    "text": "Customers",
                    "type": "text"
                },
                {
                    "element": "&",
                    "bounding_box": [
                        218,
                        1080,
                        236,
                        1100
                    ],
                    "text": "&",
                    "type": "text"
                },
                {
                    "element": "leads",
                    "bounding_box": [
                        245,
                        1080,
                        314,
                        1100
                    ],
                    "text": "leads",
                    "type": "text"
                }
            ],
            "gui_elements": [
                {
                    "element": "button",
                    "bounding_box": [
                        2.2720413,
                        1606.9541,
                        438.0704,
                        1703.7102
                    ],
                    "confidence": 0.7675509,
                    "type": "object"
                },
                {
                    "element": "button",
                    "bounding_box": [
                        2.295353,
                        1710.0834,
                        441.2123,
                        1799.217
                    ],
                    "confidence": 0.81576186,
                    "type": "object"
                }
            ],
            "clickable_coordinates": [
                73,
                1090
            ],
            "description": "Click on the 'Customers' menu item"
        }
    ]
}


time.sleep(5)

action_executor = ActionExecutor()


action_executor.execute_action(action1)




