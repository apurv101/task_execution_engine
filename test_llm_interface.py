import os
from PIL import Image, ImageDraw, ImageFont
import cv2
import json
task = "Create a new customer named Acme Corporation"

test_image_1 = "/Users/apoorvagarwal/Desktop/aimyable/system/screenshots/Screenshot 2024-09-19 at 11.41.46 PM.png"
test_image_2 = "/Users/apoorvagarwal/Desktop/aimyable/system/screenshots/Screenshot 2024-09-20 at 1.40.24 PM.png"
test_image_3 = "/Users/apoorvagarwal/Desktop/aimyable/system/screenshots/Screenshot 2024-09-20 at 1.43.29 PM.png"


from llm_interface import LLMInterface
from vision_system import VisionSystem

# open("actions_test.txt", "w").close()


google_credentials_path = "/Users/apoorvagarwal/Desktop/aimyable/system/aimyable-test-bc025e804aba.json"
yolo_model_path = "/Users/apoorvagarwal/Desktop/aimyable/system/yolov8_best.pt"


llm_interface = LLMInterface(api_key=os.getenv("API_KEY_OPEN_AI"))
vision_system = VisionSystem(google_credentials_path, yolo_model_path)

from PIL import Image, ImageDraw, ImageFont

def plot_bounding_boxes(image_path, actions, output_path):
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Define colors for different element types
    text_color = 'red'
    gui_color = 'blue'
    
    # Optionally, set up fonts for labeling
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    # Loop over each action
    for action in actions['actions']:
        # Draw bounding boxes for text elements
        for text_element in action['text_elements']:
            bbox = text_element['bounding_box']
            # bbox is [x_min, y_min, x_max, y_max]
            # Draw rectangle
            draw.rectangle(bbox, outline=text_color, width=2)
            # Annotate with element name
            label = text_element['text']
            draw.text((bbox[0], bbox[1]-15), label, fill=text_color, font=font)
        
        # Draw bounding boxes for GUI elements
        for gui_element in action['gui_elements']:
            bbox = gui_element['bounding_box']
            draw.rectangle(bbox, outline=gui_color, width=2)
            # Annotate with element name
            label = gui_element['element']
            draw.text((bbox[0], bbox[1]-15), label, fill=gui_color, font=font)


    
    # Save the image with bounding boxes
    image.save(output_path)
    print(f"Annotated image saved to {output_path}")






# from PIL import Image, ImageDraw, ImageFont

def plot_bounding_boxes_and_points(image_path, actions, output_path):
    # Open the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    
    # Define colors for different element types
    text_color = 'red'
    gui_color = 'blue'
    point_color = 'green'  # Color for the clickable point
    
    # Optionally, set up fonts for labeling
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    # Loop over each action
    for action in actions['actions']:
        # Draw bounding boxes for text elements
        for text_element in action.get('text_elements', []):
            bbox = text_element['bounding_box']
            # bbox is [x_min, y_min, x_max, y_max]
            # Draw rectangle
            draw.rectangle(bbox, outline=text_color, width=2)
            # Annotate with element name
            label = text_element.get('text', '')
            draw.text((bbox[0], bbox[1]-15), label, fill=text_color, font=font)
        
        # Draw bounding boxes for GUI elements
        for gui_element in action.get('gui_elements', []):
            bbox = gui_element['bounding_box']
            draw.rectangle(bbox, outline=gui_color, width=2)
            # Annotate with element name
            label = gui_element.get('element', '')
            draw.text((bbox[0], bbox[1]-15), label, fill=gui_color, font=font)
        
        # Draw the clickable point if available
        if 'clickable_coordinates' in action:
            x, y = action['clickable_coordinates']
            # Draw a small circle at the clickable point
            r = 5  # Radius of the circle
            draw.ellipse((x - r, y - r, x + r, y + r), fill=point_color, outline=point_color)
            # Optionally, annotate the point
            draw.text((x + 10, y - 10), "Clickable Point", fill=point_color, font=font)
    
    # Save the image with annotations
    image.save(output_path)
    print(f"Annotated image saved to {output_path}")








def plot_google_vision_output(text_elements, test_image_path, test_output_path):
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
    cv2.imwrite(test_output_path, image_text)

def yolo_vision_output(yolo_elements, test_image_path, test_output_path):
    image = cv2.imread(test_image_path)
    image_yolo = image.copy()
    for elem in yolo_elements:
        # Assuming 'bounding_box' is [x1, y1, x2, y2]
        x1, y1, x2, y2 = elem['bounding_box']
        # Draw the rectangle
        cv2.rectangle(image_yolo, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
        # Put the label
        cv2.putText(image_yolo, elem.get('label', ''), (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    # Save the image with YOLO bounding boxes
    cv2.imwrite(test_output_path, image_yolo)

all_history = []
relevant_history = []
def process_image(image_path, output_path, google_vision_path, yolo_vision_path):
    global all_history
    global relevant_history
    google_vision_elements = vision_system.detect_text(image_path)
    yolo_elements = vision_system.yolo_service(image_path)
    plot_google_vision_output(google_vision_elements, image_path, google_vision_path)
    yolo_vision_output(yolo_elements, image_path, yolo_vision_path)

    action = llm_interface.generate_next_action(
        task=task,
        google_vision_elements=google_vision_elements,
        yolo_elements=yolo_elements,
        action_history=relevant_history,
        image_path=image_path
    )
    print(action)
    # insert action in a file pretty print
    with open("actions_test.txt", "a") as f:
        f.write(json.dumps(action, indent=4))
        f.write("\n")



    plot_bounding_boxes_and_points(image_path, action, output_path)
    all_history = all_history + action['actions']
    filtered_actions = [{'action': a['action'], 'description': a['description']} for a in action['actions']]
    relevant_history = relevant_history + filtered_actions
    print("*"*100)
    print(relevant_history)



# import time


# process_image(test_image_1, 'annotated_pointed_screenshot1.png', 'google_vision1.png', 'yolo_vision1.png')
# time.sleep(10)
# process_image(test_image_2, 'annotated_pointed_screenshot2.png', 'google_vision2.png', 'yolo_vision2.png')
# time.sleep(10)
# process_image(test_image_3, 'annotated_pointed_screenshot3.png', 'google_vision3.png', 'yolo_vision3.png')


