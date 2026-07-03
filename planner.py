# planner.py

from task import Task

# --- PLANNER ---
class Planner:
    def __init__(self, memory):
        self.memory = memory
    def task_input_selector(self, part, reason):
        if reason == "math":
            self.task_input = part.replace("hesapla ", "")
        
        elif reason == "variable":
            variable = part.replace("sonucu ", "")
            variable = variable.replace(" olarak kaydet", "")
            self.task_input = variable

        elif reason == "save_name":
            self.task_input = part.replace("adım ", "")

        elif reason == "adding":
            words = part.split()
            numbers = []
            for word in words:
                if word.isdigit() or word in self.memory.variables:
                    numbers.append(word)
            self.task_input = " + ".join(numbers)

        elif reason == "research":
            self.task_input = part.replace("araştır ", "")
        
        else:
            self.task_input = part
        
        if self.task_input:
            return self.task_input


    def plan(self, reasons, next_task_id):
        tasks = []

        for reason in reasons:
            task_id = next_task_id
            intent = reason["intent"]
            part = reason["part"]
            description = intent
            task_input = self.task_input_selector(part, intent)
            task = Task(task_id, description, task_input)

            tasks.append(task)

        return tasks