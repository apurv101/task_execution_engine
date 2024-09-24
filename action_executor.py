import pyautogui

class ActionExecutor:
    def __init__(self):
        pass

    def execute_action(self, action):
        # action is a dict containing action details
        actions = action.get("actions", [])
        for act in actions:
            action_type = act.get("action")
            element = act.get("element")
            bounding_box = act.get("bounding_box", [0, 0, 0, 0])
            x = (bounding_box[0] + bounding_box[2]) / 2
            y = (bounding_box[1] + bounding_box[3]) / 2

            if action_type == "moveTo":
                pyautogui.moveTo(x, y, duration=1)
                print(f"Moved mouse to ({x}, {y}) for element {element}")

            elif action_type == "click":
                pyautogui.click(x, y)
                print(f"Clicked at ({x}, {y}) on element {element}")

            elif action_type == "doubleClick":
                pyautogui.doubleClick(x, y)
                print(f"Double-clicked at ({x}, {y}) on element {element}")

            elif action_type == "rightClick":
                pyautogui.rightClick(x, y)
                print(f"Right-clicked at ({x}, {y}) on element {element}")

            elif action_type == "type":
                value = act.get("value", "")
                pyautogui.write(value)
                print(f"Typed value: {value}")

            elif action_type == "press":
                keys = act.get("keys", [])
                pyautogui.hotkey(*keys)
                print(f"Pressed keys: {keys}")

            elif action_type == "scroll":
                amount = act.get("amount", 0)
                pyautogui.scroll(amount)
                print(f"Scrolled by {amount}")

            elif action_type == "drag":
                start_box = act.get("start_bounding_box", [0, 0, 0, 0])
                end_box = act.get("end_bounding_box", [0, 0, 0, 0])
                start_x = (start_box[0] + start_box[2]) / 2
                start_y = (start_box[1] + start_box[3]) / 2
                end_x = (end_box[0] + end_box[2]) / 2
                end_y = (end_box[1] + end_box[3]) / 2
                pyautogui.moveTo(start_x, start_y)
                pyautogui.dragTo(end_x, end_y, duration=0.5)
                print(f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")

            else:
                print(f"Unknown action type: {action_type}")
