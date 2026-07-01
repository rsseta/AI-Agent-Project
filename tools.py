from memory import history, variables, researches, save_data, get_data, get_memory, save_json, save_used
import datetime as dt
from ddgs import DDGS

def get_time():
    return dt.datetime.now().strftime('%H:%M:%S')

def calculate(msg):
    try:
        try:
            tokens = msg.split()
            resolved = ""
            for t in tokens:
                if t in variables:
                    resolved += f"{variables[t]} "
                else:
                    resolved += t
            msg = resolved
        except Exception as e:
            print(e)
        result = eval(msg)
        save_data("last_result", result)
        return f"Sonuç -> {result}"
    except Exception as e:
        return f"Hesaplama Hatası: {e}"

def get_memory_count():
    return len(history.get_memory())

def save_name(msg):
    name = msg.replace("adım ", "")
    save_data("name", name)
    return f"Adın {name} olarak kaydedildi!"
    
def get_name():
    try:
        name = get_data("name")
        return f"Adın {name}"
    except Exception as e:
        return e
    
def last_msg():
    user_messages = [
        msg for msg in get_memory()
        if msg["role"] == "user"
    ]
    if len(user_messages) >= 2:
        return user_messages[-2]['content']
    else:
        return "Henüz öcenki mesajınız yok"
    
def search_memory(keyword):
    user_messages = [
        msg for msg in get_memory()
        if msg["role"] == "user"
        and keyword in msg["content"]
    ]
    if not user_messages:
        return f"{keyword} içeren mesaj bulunamadı"
    return f"{keyword} içeren {len(user_messages)} sonuç -> {', '.join([msg['content'] for msg in user_messages])}"

def repeat():
    last_input = get_data("last_input")
    last_tool = get_data("last_tool")
    if last_msg() and get_data("last_tool"):
        return last_tool, last_input
    else:
        return None
    
def save_result():
    try:
        last_result = get_data("last_result")
        save_data("saved_result", last_result)
        return f"{last_result} sonucu kaydedildi."
    except Exception as e:
        return f"Sonuç bulunamadı, kaydedilemedi: {e}"

def show_result():
    result = get_data("saved_result")
    if result:
        return f"Kaydedilen sonuç -> {result}"
    else:
        return "Henüz bir sonuç kaydedilmedi"
    
def exit():
    return quit()

def save_variable(variable):
    last = get_data("last_result")
    if last == None:
        return "Son sonuç bulunmuyor."
    variables[variable] = last
    save_json()
    return f"{variable}, {last} olarak kaydedildi."

def show_variables():
    if not variables:
        return "Değişken yok"

    response = ""
    for variable, value in variables.items():
        response += f"{variable} = {value}, "

    return response

def ddgs(key):
    try:
        with DDGS() as ddg:
            results = list(ddg.text(key, max_results=3))
            return results
    except Exception as e:
        return f"ddgs hatası: {e}"

#Search
def web_search(key):
    if key in researches:
        first = results[0]
        result = first.get("body", "No content")[:1000]
        source = first.get("href", "unknown")
        times_used = researches[key]["times_used"]
        times_used += 1
        save_used(key, times_used)
        return result
    
    date = dt.datetime.now()

    try:
        results = ddgs(key)
        if not results:
            return "Sonuç Bulunamadı"
        
        result = results[0]["body"][:1000]
        source = f"ddgs({results[0]['href']})"
    
    except Exception as e:
        return f"Araştırma hatası: {str(e)}"
    
    researches[key] = {
        "content": result,
        "source": source,
        "times_used": 1,
        "saved_at": str(date),
        "query": key
    }

    return result

    

    
    
    