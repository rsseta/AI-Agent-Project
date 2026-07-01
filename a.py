import json
import datetime as dt
from ddgs import DDGS
from intent import detect_intent

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


class Memory:
    def __init__(self):
        self.data = {}
        self.history = []
        self.saved_data = {}
        self.variables = {}
        self.researches = {}

    def load_memory(self):
        try:
            with open("memory.json", "r") as file:
                data = json.load(file)
                self.variables.update(data.get("variables", []))
                self.researches.update(data.get("researches", []))
                self.saved_data.update(data.get("saved_data", []))
        except:
            print("Data Alınamadı!")

        try:
            with open("history.json", "r") as file:
                self.history.extend(data.get("history", []))
        except:
            print("History alınamadı!")

    def save(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })
        self.save_history()

    def save_data(self, key, value):
        self.saved_data[key] = value
        self.save_json()

    def get_data(self, key):
        return self.saved_data.get(key)

    def get_memory(self):
        return self.history

    def last_message(self):
        if self.history:
            return self.history[-1]

        return None

    def save_json(self):
        data = {
            "saved_data": self.saved_data,
            "variables": self.variables,
            "researches": self.researches,
        }
        with open("memory.json", "w") as file:
            json.dump(data, file, indent=4)
            # print(f"Yazdım: {data}")

    def save_history(self):
        with open("history.json", "w") as file:
            json.dump(self.history, file, indent=4)

    def save_used(self, key, value):
        self.researches[key]["times_used"] = value
        self.save_json()

class Reasoner:
    def analyze(self, msg):
        msg = msg.lower()
        parts = [part.strip() for part in msg.split(" ve ")]
        intents = []
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
    
    def result(self, tasks):
        results = ""
        for task in tasks:
            # print(f"Task: task_id={task.task_id}, description={task.description}, input={task.input}, output={task.output}, status={task.status}")
            results += f"{task.output}. " 
        return results

class Tools:

    def get_time(self):
        return dt.datetime.now().strftime('%H:%M:%S')

    def calculate(self, msg):
        try:
            try:
                tokens = msg.split()
                resolved = ""
                for t in tokens:
                    if t in self.memory.variables:
                        resolved += f"{self.memory.variables[t]} "
                    else:
                        resolved += t
                msg = resolved
            except Exception as e:
                print(e)
            result = eval(msg)
            self.memory.save_data("last_result", result)
            return f"Sonuç -> {result}"
        except Exception as e:
            return f"Hesaplama Hatası: {e}"

    def get_memory_count(self):
        return len(self.memory.history.get_memory())

    def save_name(self, msg):
        name = msg.replace("adım ", "")
        self.memory.save_data("name", name)
        return f"Adın {name} olarak kaydedildi!"
        
    def get_name(self):
        try:
            name = self.memory.get_data("name")
            return f"Adın {name}"
        except Exception as e:
            return e
        
    def last_msg(self):
        user_messages = [
            msg for msg in self.memory.get_memory()
            if msg["role"] == "user"
        ]
        if len(user_messages) >= 2:
            return user_messages[-2]['content']
        else:
            return "Henüz öcenki mesajınız yok"
        
    def search_memory(self, keyword):
        user_messages = [
            msg for msg in self.memory.get_memory()
            if msg["role"] == "user"
            and keyword in msg["content"]
        ]
        if not user_messages:
            return f"{keyword} içeren mesaj bulunamadı"
        return f"{keyword} içeren {len(user_messages)} sonuç -> {', '.join([msg['content'] for msg in user_messages])}"

    def repeat(self):
        last_input = self.memory.get_data("last_input")
        last_tool = self.memory.get_data("last_tool")
        if self.last_msg() and self.memory.get_data("last_tool"):
            return last_tool, last_input
        else:
            return None
        
    def save_result(self):
        try:
            last_result = self.memory.get_data("last_result")
            self.memory.save_data("saved_result", last_result)
            return f"{last_result} sonucu kaydedildi."
        except Exception as e:
            return f"Sonuç bulunamadı, kaydedilemedi: {e}"

    def show_result(self):
        result = self.memory.get_data("saved_result")
        if result:
            return f"Kaydedilen sonuç -> {result}"
        else:
            return "Henüz bir sonuç kaydedilmedi"
        
    def exit(self):
        return quit()

    def save_variable(self, variable):
        last = self.memory.get_data("last_result")
        if last == None:
            return "Son sonuç bulunmuyor."
        self.memory.variables[variable] = last
        self.memory.save_json()
        return f"{variable}, {last} olarak kaydedildi."

    def show_variables(self):
        if not self.memory.variables:
            return "Değişken yok"

        response = ""
        for variable, value in self.memory.variables.items():
            response += f"{variable} = {value}, "

        return response

    def ddgs(self, key):
        try:
            with DDGS() as ddg:
                results = list(ddg.text(key, max_results=3))
                return results
        except Exception as e:
            return f"ddgs hatası: {e}"

    #Search
    def web_search(self, key):
        if key in self.memory.researches:
            first = self.memory.researches[key]
            result = first.get("body", "No content")[:1000]
            source = first.get("href", "unknown")
            times_used = self.memory.researches[key]["times_used"]
            times_used += 1
            self.memory.save_used(key, times_used)
            return result
        
        date = dt.datetime.now()

        try:
            results = self.ddgs(key)
            if not results:
                return "Sonuç Bulunamadı"
            
            result = results[0]["body"][:1000]
            source = f"ddgs({results[0]['href']})"
        
        except Exception as e:
            return f"Araştırma hatası: {str(e)}"
        
        self.memory.researches[key] = {
            "content": result,
            "source": source,
            "times_used": 1,
            "saved_at": str(date),
            "query": key
        }

        return result

class ToolManager:
    def __init__(self, memory):
        self.memory = memory
        self.tools = Tools()

        self.tool_dict = {
            name: getattr(self.tools, name)
            for name in dir(self.tools)
            if not name.startswith("_")
            and callable(getattr(self.tools, name))
        }

    def run_tool(self, task, msg):
        if task not in self.tools:
            return None
            
        elif task == "memory_count":
            return f"Toplam {self.tools[task]()} mesaj var."
        
        elif task == "last_message":
            data = self.tools[task]()
            if data == None:
                return "Son mesajınız yok"
            return "Son mesajınız işlem için uygunsuz"
        
        elif task == "search_memory":
            keyword = msg.replace("ara ", "")
            return self.tools[task](keyword)
        
        elif task == "repeat":
            last_tool, last_input = self.tools[task]()
            return self.run_tool(last_tool, last_input)
        
        elif task == "intent_search":
            if "hesaplama" in msg:
                return self.tools["search_memory"]("hesapla")
            
        elif task in ["variable", "research", "save_name", "math"]:
            return self.tools[task](msg)  
            
        return self.tools[task]()

    def run(self, task):
        if task.description in self.tools:
            task.tool = task.description

        if task.tool == None or task.tool not in self.tools:
            return None
        
        if task.tool in self.tools:
            task.status = "RUNNING"
            output = self.run_tool(task.tool, task.input)
            return output

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

# Kullanıcı Döngüsü
agent = Agent()

while True:
    agent.memory.load_memory()

    msg = input("Yaz: ")
    print(f"Bot: {agent.process(msg)}")
    print("-"*225)