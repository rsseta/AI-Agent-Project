#a.py

from memory import Memory
from planner import Planner
from toolmanager import ToolManager
from intent import detect_intent


class Reasoner:
    def analyze(self, msg):

        # Cut Msg
        msg = msg.lower()
        parts = [part.strip() for part in msg.split(" ve ")]

        intents = []

        # Return Part and Intent
        for part in parts:
            intent = detect_intent(part)
            intents.append({"part": part, "intent": intent})
        return intents
    
    def state_control(self, tasks):
        if len(tasks) == 0:
            return None
        else:
            return "READY"
        # task = tasks[-1]
        # output = task.output
        # if output is None or output == "":
        #     task.restart()
    

# --- EXECUTOR ---
class Executor:
    def execute(self, task, toolMan):

        # Beklemedeyse çalıştır
        if task.status == "PENDING" or task.status == "RETRYING":
            run = toolMan.run(task)

            # Hata çıkarsa tekrar dene
            if run == None:
                task.retry()
            else:
                task.output = run
                task.status = "COMPLETED"
    
    # Create Response on Outputs
    def result(self, tasks):
        results = ""
        for task in tasks:
            # print(f"Task: task_id={task.task_id}, description={task.description}, input={task.input}, output={task.output}, status={task.status}")
            results += f"{task.output}. " 
        return results


# --- AGENT ---
class Agent:
    def __init__(self):
        self.tasks = []
        self.next_task_id = 0
        self.memory = Memory()
        self.reasoner = Reasoner()
        self.planner = Planner(self.memory)
        self.executor = Executor()
        self.tool_manager = ToolManager(self.memory)
    
    # İşleme
    def process(self, msg):
        goal = self.reasoner.analyze(msg)

        self.tasks = self.planner.plan(goal, self.next_task_id)

        for task in self.tasks:
            self.state = self.reasoner.state_control(self.tasks)
            if self.state == None:
                return "Anlayamadım"
            
            self.executor.execute(task, self.tool_manager)
            self.next_task_id += 1
        
        return self.executor.result(self.tasks)


agent = Agent()

# Kullanıcı Döngüsü
while True:
    agent.memory.load_memory()

    msg = input("Yaz: ")
    print(f"Bot: {agent.process(msg)}")
    print("-"*225)