class Tools:

    def __init__(self, memory):
        self.memory = memory

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