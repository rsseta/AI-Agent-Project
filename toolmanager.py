# toolmanager.py

import inspect
import tools
from basetool import BaseTool

# --- TOOLS ---

class ToolManager:
    def __init__(self, memory):

        self.tools = {}

        for _, cls in inspect.getmembers(tools, inspect.isclass):
            if issubclass(cls, BaseTool) and cls is not BaseTool:
                tool = cls(memory)
                self.tools[tool.name] = tool

    def run_tool(self, task, msg):

        if task not in self.tools:
            return None
        
        elif task == "repeat":
            last_tool, last_input = self.tools[task].run()
            return self.run_tool(last_tool, last_input)
        
        elif task in ["variable", "research", "save_name", "math", "search_memory", "intent_search"]:
            return self.tools[task].run(msg) 
            
        return self.tools[task].run()

    def run(self, task):
        if task.description in self.tools:
            task.tool = task.description

        if task.tool == None or task.tool not in self.tools:
            return None
        
        if task.tool in self.tools:
            task.status = "RUNNING"
            output = self.run_tool(task.tool, task.input)
            return output