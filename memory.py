#memory.py

import json

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