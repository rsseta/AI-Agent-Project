from memory import load_memory, save, save_data
from planner import make_task_plan
from tools import get_time, calculate, get_memory_count, save_name, get_name, last_msg, search_memory, repeat, save_result, show_result, exit, save_variable, show_variables, web_search
import datetime as dt
tools = {
    "time": get_time,
    "math": calculate,
    "memory_count": get_memory_count,
    "save_name": save_name,
    "get_name": get_name,
    "search_memory": search_memory,
    "last_message": last_msg,
    "repeat": repeat,
    "save_result": save_result,
    "show_result": show_result,
    "variable": save_variable,
    "show_variables": show_variables,
    "research": web_search,
    "exit": exit,
}

#tool Çalıştır
def run_tool(task, msg):
    if task not in tools:
        return None
        
    elif task == "memory_count":
        return f"Toplam {tools[task]()} mesaj var."
    
    elif task == "last_message":
        data = tools[task]()
        if data == None:
            return "Son mesajınız yok"
        return "Son mesajınız işlem için uygunsuz"
    
    elif task == "search_memory":
        keyword = msg.replace("ara ", "")
        return tools[task](keyword)
    
    elif task == "repeat":
        last_tool, last_input = tools[task]()
        return run_tool(last_tool, last_input)
    
    elif task == "intent_search":
        if "hesaplama" in msg:
            return tools["search_memory"]("hesapla")
        
    elif task in ["variable", "research", "save_name", "math"]:
        return tools[task](msg)  
        
    return tools[task]()

# Hafıza
load_memory()

# Yaşam Döngüsü
while True:
    msg = input("Sen: ")
    save("user", msg)

    tasks = []
    results = []
    plan = make_task_plan(msg)

    for step in plan:
        task = step["task"]
        try:
            task_input = step["input"]
        except:
            task_input = None
        
        tasks.append(task)
        if task_input is not None:
            result = run_tool(task, task_input)
        else:
            result = run_tool(task, "")

        if result:
            results.append(f"Bot: {result}")

    responses = "\n".join(results)

    if task != "repeat": 
        save_data("last_tool", task)
        save_data("last_input", msg)
    else:
        save_data("last_tool", tasks[-2] if len(tasks) >= 2 else None)
        save_data("last_input", plan[-2] if len(plan) >= 2 else None)
        
    if responses:
        print(responses)
        save("assistant", str(responses))
    
    print(f"\n{'-'*10000}\n")