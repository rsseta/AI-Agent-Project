from intent import detect_intent
from old_useless.memory import get_data, variables

def make_plan(task):

    if task == "math":
        return [
            "ifadeyi al",
            "hesap yap",
            "sonucu döndür"
        ]
    elif task == "time":
        return [
            "saat bilgisini al",
            "sonucu döndür"
        ]
    elif task == "greeting":
        return [
            "selamlaşma mesajı oluştur",
            "sonucu döndür"
        ]
    elif task == "save_name":
        return [
            "adı kaydet",
            "sonucu döndür"
        ]
    elif task == "get_name":
        return [
            "adı al",
            "sonucu döndür"
        ]
    else:
        return [
            "Bilinmeyen görev, plan oluşturulamıyor"
        ]

def make_task_plan(msg):

    msg = msg.lower()

    plan = []

    parts = [part.strip() for part in msg.split(" ve ")]
    for part in parts:
        task_input = None
        task = detect_intent(part)

        if task == "math":
            task_input = part.replace("hesapla ", "")

        elif task == "save_result":
            get_data("last_result")
        
        elif task == "variable":
            variable = part.replace("sonucu ", "")
            variable = variable.replace(" olarak kaydet", "")
            task_input = variable

        elif task == "save_name":
            task_input = part.replace("adım ", "")

        elif task == "adding":
            task = "math"
            words = part.split()
            numbers = []
            for word in words:
                if word.isdigit() or word in variables:
                    numbers.append(word)
            task_input = " + ".join(numbers)

        elif task == "research":
            task_input = part.replace("araştır ", "")
            


        if task_input is not None:
            plan.append({
                "task": task,
                "input": task_input
            })
        else:
            plan.append({
                "task": task
            })

        
    # print(plan)

    return plan