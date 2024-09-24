actions1 = {'actions': [{'action': 'moveTo', 'element': 'Add customer', 'bounding_box': [646, 1126, 723, 1146], 'description': "Move mouse to the 'Add customer' button to prepare for adding a new customer."}, {'action': 'click', 'element': 'Add customer', 'bounding_box': [646, 1126, 723, 1146], 'description': "Click on the 'Add customer' button to open the form for creating a new customer."}]}

from action_executor import ActionExecutor
import pyautogui

executor = ActionExecutor()

# sleep for 5 seconds
import time
time.sleep(2)

pyautogui.moveTo(500, 500, duration=1)

time.sleep(5)

executor.execute_action(actions1)




actions2 = {'actions': [{'action': 'moveTo', 'element': 'Company name input field', 'bounding_box': [1526, 1284, 1602, 1309], 'description': "Move mouse to the 'Company name' input field to prepare for typing the customer name."}, {'action': 'type', 'element': 'Company name input field', 'text': 'GOOGLE ADS TRAINING AND CONSULTING LLC', 'description': "Type 'GOOGLE ADS TRAINING AND CONSULTING LLC' into the 'Company name' input field to create a new customer."}]}



