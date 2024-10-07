import time
import json
import os
# Import the necessary modules
from llm_interface import LLMInterface
from vision_system import VisionSystem
from action_executor import ActionExecutor
from action_history import ActionHistory
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

from visualize import plot_bounding_boxes_and_points, plot_google_vision_output, yolo_vision_output


google_credentials_path = r"C:\Users\apoor\OneDrive\Desktop\aimyable\task_execution_engine\aimyable-test-bc025e804aba.json"
yolo_model_path = r"C:\Users\apoor\OneDrive\Desktop\aimyable\task_execution_engine\yolov8_best.pt"

# google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# yolo_model_path = r"C:\Users\apoor\OneDrive\Desktop\aimyable\task_execution_engine\yolov8_best.pt"

print("Hello!!")


# Empty actions_test.txt
open("actions_test.txt", "w").close()

def main():
    time.sleep(5)  # Wait for the user to switch to the target application
    # Initialize components
    llm_interface = LLMInterface(api_key=os.getenv("API_KEY_OPEN_AI"))
    vision_system = VisionSystem(google_credentials_path, yolo_model_path)
    action_executor = ActionExecutor()
    action_history = ActionHistory()




    

    # Define the task
    task_description = "Create a new customer named Acme Corporation"

    # Initialize variables
    task_finished = False

    k = 0

    while not task_finished:
        print("\n--- New Iteration ---")

        # 1. Take a screenshot
        screenshot_path = "current_screenshot.png"
        vision_system.take_screenshot(screenshot_path)

        # 2. Extract GUI elements
        google_vision_elements = vision_system.detect_text(screenshot_path)
        yolo_elements = vision_system.yolo_service(screenshot_path)

        # Plot the bounding boxes and points
        
        plot_google_vision_output(google_vision_elements, screenshot_path, f"images/action_google_vision_{k}.png")
        yolo_vision_output(yolo_elements, screenshot_path, f"images/action_yolo_{k}.png")

        # 3. Get action history
        history = action_history.get_history()

        # 4. Generate the next action using the LLM
        action = llm_interface.generate_next_action(
            task=task_description,
            google_vision_elements=google_vision_elements,
            yolo_elements=yolo_elements,
            action_history=history,
            image_path=screenshot_path
        )

        ## add action to a file
        with open("actions_test.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(action, indent=4))
            f.write("\n")

        plot_bounding_boxes_and_points(screenshot_path, action, f"images/action_annotated_screenshot_{k}.png")

        print("Action generated:", action)


        # 5. Execute the action
        task_finished = action_executor.execute_action(action)

        print("Task finished:")



        # 6. Update action history
        action_history.add_action(action)

        # 7. Wait before the next iteration
        time.sleep(30)  # Adjust the sleep time as needed

        k += 1

    print("Task completed successfully!")

if __name__ == "__main__":
    main()
