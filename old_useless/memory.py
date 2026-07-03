import json

history = []
saved_data = {}
variables = {}
researches = {}

def load_memory():
    global saved_data, variables
    
    try:
        with open("memory.json", "r") as file:
            data = json.load(file)
            variables.update(data.get("variables", []))
            researches.update(data.get("researches", []))
            saved_data.update(data.get("saved_data", []))
    except:
        print("Data Alınamadı!")

    try:
        with open("history.json", "r") as file:
            history.extend(data.get("history", []))
    except:
        print("History alınamadı!")

def save(role, content):
    history.append({
        "role": role,
        "content": content
    })
    save_history()

def save_data(key, value):
    saved_data[key] = value
    save_json()

def get_data(key):
    return saved_data.get(key)

def get_memory():
    return history

def last_message():
    if history:
        return history[-1]

    return None

def save_json():
    data = {
        "saved_data": saved_data,
        "variables": variables,
        "researches": researches,
    }
    with open("memory.json", "w") as file:
        json.dump(data, file, indent=4)
        # print(f"Yazdım: {data}")

def save_history():
    with open("history.json", "w") as file:
        json.dump(history, file, indent=4)

def save_used(key, value):
    researches[key]["times_used"] = value
    save_json()