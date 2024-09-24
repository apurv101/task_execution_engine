import time
from task_planner import TaskPlanner
from vision_system import VisionSystem
from llm_interface import LLMInterface
from action_executor import ActionExecutor
from action_history import ActionHistory
from plan_updater import PlanUpdater
import os

def main():


    # Paths to credentials and YOLO model
    google_credentials_path = "/Users/apoorvagarwal/Desktop/aimyable/system/aimyable-test-bc025e804aba.json"
    yolo_model_path = "/Users/apoorvagarwal/Desktop/aimyable/system/yolov8_best.pt"



    # Initialize components
    llm_interface = LLMInterface(api_key=os.getenv("API_KEY_OPEN_AI"))
    task_planner = TaskPlanner(llm_interface)
    vision_system = VisionSystem(google_credentials_path, yolo_model_path)
    action_executor = ActionExecutor()
    action_history = ActionHistory()
    plan_updater = PlanUpdater(llm_interface)

    # Get task description
    task_description = "Quickbooks is open. Please create a new invoice for the client 'Apurv Agarwal' with the following details: Invoice Number: INV-123, Date: 2022-01-15, Amount: $500."

    # Generate plan
    # plan = task_planner.generate_plan(task_description)

    task_accomplished = False
    while not task_accomplished:
        # Take screenshot
        screenshot_path = "current_screenshot.png"
        vision_system.take_screenshot(screenshot_path)

       # Extract GUI elements separately
        google_vision_elements = vision_system.extract_google_vision_elements(screenshot_path)
        yolo_elements = vision_system.extract_yolo_elements(screenshot_path)


        # Get action history
        history = action_history.get_history()

        # Generate next action
        action = llm_interface.generate_next_action(
            task_description,
            google_vision_elements,
            yolo_elements,
            history
        )

        # Execute action
        action_executor.execute_action(action)

        # Update action history
        action_history.add_action(action)

        # Update plan if necessary
        # plan = plan_updater.update_plan(plan, action_history.get_history())

        # Check if the task is accomplished
        if action.get("actions", [{}])[0].get("action") == "finish":
            task_accomplished = True

        # Wait before next iteration
        time.sleep(5)

if __name__ == "__main__":
    main()
