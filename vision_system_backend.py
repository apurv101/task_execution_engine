import pyautogui
from google.cloud import vision
import io
import os
from google.protobuf.json_format import MessageToDict
from ultralytics import YOLO
from PIL import Image

class VisionSystem:
    def __init__(self, google_credentials_path, yolo_model_path):
        # Set environment variables for Google Vision API
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path
        os.environ['GRPC_DNS_RESOLVER'] = 'native'  # For Windows compatibility if needed

        # Initialize Google Vision client
        self.vision_client = vision.ImageAnnotatorClient()

        # Initialize YOLO model
        self.yolo_model = YOLO(yolo_model_path)

    def take_screenshot(self, path):
        screenshot = pyautogui.screenshot()
        screenshot.save(path)
        print(f"Screenshot saved to {path}")

    def detect_text(self, image: Image.Image):
        """Uses Google Vision API to detect text in the image."""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        content = buffered.getvalue()

        vision_image = vision.Image(content=content)

        # Perform text detection
        response = self.vision_client.text_detection(image=vision_image)
        texts = response.text_annotations

        if response.error.message:
            raise Exception(f'{response.error.message}')

        gui_elements = []

        # Skip the first element as it contains the full text
        for text in texts[1:]:
            description = text.description
            vertices = text.bounding_poly.vertices
            x_coords = [vertex.x for vertex in vertices]
            y_coords = [vertex.y for vertex in vertices]
            x_min = min(x_coords)
            x_max = max(x_coords)
            y_min = min(y_coords)
            y_max = max(y_coords)
            gui_element = {
                'element': description,
                'bounding_box': [x_min, y_min, x_max, y_max],
                'text': description,
                'type': 'text'
            }
            gui_elements.append(gui_element)

        return gui_elements
    
    def yolo_service(self, image: Image.Image):
        """Uses YOLO model to detect GUI elements in the image."""
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_bytes = buffered.getvalue()

        # YOLO can accept image bytes directly via the 'source' parameter as a BytesIO object
        results = self.yolo_model.predict(source=image, save=False, conf=0.1)
        gui_elements = []

        for result in results:
            boxes = result.boxes  # Boxes object
            for box in boxes:
                # Get coordinates and class
                xyxy = box.xyxy.cpu().numpy()[0]
                cls = int(box.cls.cpu().numpy()[0])
                conf = box.conf.cpu().numpy()[0]
                label = self.yolo_model.names[cls]
                x_min = xyxy[0]
                y_min = xyxy[1]
                x_max = xyxy[2]
                y_max = xyxy[3]
                gui_element = {
                    'element': label,
                    'bounding_box': [x_min, y_min, x_max, y_max],
                    'confidence': conf,
                    'type': 'object'
                }
                gui_elements.append(gui_element)
        return gui_elements

    def extract_gui_elements(self, screenshot_path):
        """Combines text and object detection to extract GUI elements."""
        # Detect text elements
        text_elements = self.detect_text(screenshot_path)
        # Detect GUI objects
        yolo_elements = self.yolo_service(screenshot_path)
        # Combine both lists
        gui_element_list = text_elements + yolo_elements
        return gui_element_list