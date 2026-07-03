#basetool.py

class BaseTool:
    name = ""
    def __init__(self, memory):
        self.memory = memory

    def run(self):
        raise NotImplementedError