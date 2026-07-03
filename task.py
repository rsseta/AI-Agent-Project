#task.py

class Task:
    def __init__(self, id, description, input):
        self.task_id = id
        self.description = description
        self.input = input
        self.error = None
        self.retry_count = 0
        self.output = None
        self.tool = None
        self.status = "PENDING"
        
    def retry(self):
        if self.retry_count < 3:
            self.status = "RETRYING"
            self.retry_count += 1
        else:
            self.status = "FAILED"
            return "MAX"