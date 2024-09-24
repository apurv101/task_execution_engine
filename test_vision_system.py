import cv2
import numpy as np
from vision_system import VisionSystem
import time

def main():
    # Paths to your Google credentials and YOLO model
    google_credentials_path = "/Users/apoorvagarwal/Desktop/aimyable/system/aimyable-test-bc025e804aba.json"
    yolo_model_path = "/Users/apoorvagarwal/Desktop/aimyable/system/yolov8_best.pt"
    
    # Initialize the VisionSystem
    vision_system = VisionSystem(google_credentials_path, yolo_model_path)
    
    # Choose a test image or capture a screenshot
    # Option 1: Use an existing image
    test_image_path = "/Users/apoorvagarwal/Desktop/aimyable/system/screenshots/Screenshot 2024-09-19 at 11.41.46 PM.png"
    
    # Option 2: Capture a new screenshot
    # test_image_path = "test_screenshot.png"
    # vision_system.take_screenshot(test_image_path)
    
    # Test text detection
    print("Testing Google Vision text detection...")
    text_elements = vision_system.detect_text(test_image_path)
    print("Text elements detected:")
    for elem in text_elements:
        print(elem)
    
    # Test YOLO object detection
    print("\nTesting YOLO object detection...")
    yolo_elements = vision_system.yolo_service(test_image_path)
    print("YOLO elements detected:")
    for elem in yolo_elements:
        print(elem)
    
    # Load the image
    image = cv2.imread(test_image_path)
    
    # Plot Google Vision text detections
    image_text = image.copy()
    for elem in text_elements:
        # Assuming 'bounding_box' is [x1, y1, x2, y2]
        x1, y1, x2, y2 = elem['bounding_box']
        # Draw the rectangle
        cv2.rectangle(image_text, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        # Put the text label
        cv2.putText(image_text, elem.get('text', ''), (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    # Save the image with text bounding boxes
    cv2.imwrite('text_elements.png', image_text)
    print("Image with text elements saved as 'text_elements.png'")
    
    # Plot YOLO detections
    image_yolo = image.copy()
    for elem in yolo_elements:
        # Assuming 'bounding_box' is [x1, y1, x2, y2]
        x1, y1, x2, y2 = elem['bounding_box']
        # Draw the rectangle
        cv2.rectangle(image_yolo, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
        # Put the label
        cv2.putText(image_yolo, elem.get('label', ''), (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    # Save the image with YOLO bounding boxes
    cv2.imwrite('yolo_elements.png', image_yolo)
    print("Image with YOLO elements saved as 'yolo_elements.png'")

if __name__ == "__main__":
    # Sleep for 3 seconds
    time.sleep(3)
    main()
