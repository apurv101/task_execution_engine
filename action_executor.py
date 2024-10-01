import pyautogui
import time

from PIL import Image


screenshot_path = "current_screenshot.png"
image = Image.open(screenshot_path)
image_width, image_height = image.size


screen_width, screen_height = pyautogui.size()

scale_x = screen_width / image_width
scale_y = screen_height / image_height



class ActionExecutor:
    def __init__(self):
        pass

    def execute_action(self, actions):
        actions = actions.get("actions", [])
        for act in actions:
            action_type = act.get("action")
            description = act.get("description", "")
            print(f"Executing action: {action_type} - {description}")
            
            # Handle 'moveTo' action
            if action_type == "moveTo":
                coordinates = act.get("clickable_coordinates")
                if coordinates:
                    x, y = coordinates

                    # Scale the coordinates if needed
                    x = int(x * scale_x)
                    y = int(y * scale_y)

                    print("Mouse has to move")
                    
                    print(x,y)
                    # x = x/2
                    # y = y/2
                    pyautogui.moveTo(x, y, duration=0.25)
                    print(f"Moved mouse to ({x}, {y})")
                else:
                    print("Error: 'clickable_coordinates' not provided for 'moveTo' action")

            # Handle 'click' action
            elif action_type == "click":
                # coordinates = act.get("clickable_coordinates")
                pyautogui.click()

            # Handle 'doubleClick' action
            elif action_type == "doubleClick":
                coordinates = act.get("clickable_coordinates")
                if coordinates:
                    x, y = coordinates
                    pyautogui.doubleClick()
                    print(f"Double-clicked at ({x}, {y})")
                else:
                    print("Error: 'clickable_coordinates' not provided for 'doubleClick' action")

            # Handle 'rightClick' action
            elif action_type == "rightClick":
                coordinates = act.get("clickable_coordinates")
                if coordinates:
                    x, y = coordinates
                    pyautogui.rightClick()
                    print(f"Right-clicked at ({x}, {y})")
                else:
                    print("Error: 'clickable_coordinates' not provided for 'rightClick' action")

            # Handle 'scroll' action
            elif action_type == "scroll":
                amount = act.get("amount")
                if amount is not None:
                    pyautogui.scroll(amount//2)
                    print(f"Scrolled by {amount}")
                else:
                    print("Error: 'amount' not provided for 'scroll' action")

            # Handle 'type' action
            elif action_type == "type":
                text = act.get("text")
                if text is not None:
                    coordinates = act.get("clickable_coordinates")
                    if coordinates:
                        x, y = coordinates
                        pyautogui.click()  # Click to focus the input field
                        time.sleep(0.2)  # Brief pause to ensure focus
                    pyautogui.write(text)
                    print(f"Typed text: {text}")
                else:
                    print("Error: 'text' not provided for 'type' action")

            # Handle 'press' action
            elif action_type == "press":
                keys = act.get("keys")
                if keys:
                    if isinstance(keys, list):
                        pyautogui.hotkey(*keys)
                        print(f"Pressed keys: {keys}")
                    else:
                        pyautogui.press(keys)
                        print(f"Pressed key: {keys}")
                else:
                    print("Error: 'keys' not provided for 'press' action")

            # Handle 'drag' action
            elif action_type == "drag":
                start_coordinates = act.get("start_coordinate")
                end_coordinates = act.get("end_coordinate")
                duration = act.get("duration", 0.5)
                if start_coordinates and end_coordinates:
                    start_x, start_y = start_coordinates
                    end_x, end_y = end_coordinates
                    pyautogui.moveTo(start_x, start_y)
                    pyautogui.dragTo(end_x, end_y, duration=duration)
                    print(f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
                else:
                    print("Error: 'start_coordinate' or 'end_coordinate' not provided for 'drag' action")

            # Handle 'finish' action
            elif action_type == "finish":
                print("Task finished.")
                # Return True to indicate that the task is completed
                return True

            else:
                print(f"Unknown action type: {action_type}")
        # Return False to indicate that the task is not yet completed
        return False
