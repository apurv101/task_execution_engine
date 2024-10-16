# mock_vision_system.py

import pyautogui
import io
from PIL import Image

class VisionSystem:
    def __init__(self, google_credentials_path, yolo_model_path):
        # Mock initialization
        print("Initialized MockVisionSystem (mocked).")
    
    def take_screenshot(self, path):
        # Mock screenshot taking
        print(f"Mock screenshot saved to {path}")
    
    def detect_text(self, image: Image.Image):
        """Mocks text detection by returning static text elements."""
        print("Mock detecting text in image.")
        # Return a fixed list of text elements
        return [
            {
                'element': 'File',
                'bounding_box': [10, 10, 50, 30],
                'text': 'File',
                'type': 'text'
            },
            {
                'element': 'Edit',
                'bounding_box': [60, 10, 100, 30],
                'text': 'Edit',
                'type': 'text'
            },
            {
                'element': 'View',
                'bounding_box': [110, 10, 150, 30],
                'text': 'View',
                'type': 'text'
            }
        ]
    
    def yolo_service(self, image: Image.Image):
        """Mocks object detection by returning static GUI elements."""
        print("Mock detecting GUI elements in image using YOLO.")
        # Return a fixed list of GUI elements
        return [
            {
                'element': 'button',
                'bounding_box': [200, 150, 250, 200],
                'confidence': 0.95,
                'type': 'object'
            },
            {
                'element': 'icon',
                'bounding_box': [300, 250, 350, 300],
                'confidence': 0.90,
                'type': 'object'
            }
        ]
    
    def extract_gui_elements(self, screenshot_path):
        """Mocks extraction of GUI elements by combining mock text and object detections."""
        print("Mock extracting GUI elements from screenshot.")
        # Return combined list of mock elements
        text_elements = self.detect_text(None)
        yolo_elements = self.yolo_service(None)
        return text_elements + yolo_elements