from llm_interface import generate_prompt

class TaskPlanner:
    def __init__(self, llm_interface):
        self.llm_interface = llm_interface
        self.plan = None

    def generate_plan(self, task_description):
        prompt = generate_prompt(task_description)
        self.plan = self.llm_interface.generate_long_term_plan(prompt)
        return self.plan
