def think(task, msg):

    thoughts = []

    thoughts.append(f"Gelen görev: {task}")

    if task == "math":
        thoughts.append("Matematik işlemi yapılacak")

    elif task == "time":
        thoughts.append("Saat bilgisi alınacak")

    elif task == "greeting":
        thoughts.append("Kullanıcı selamlaşıyor")

    elif task == "save_name":
        thoughts.append("Kullanıcı adını belirtti")

    elif task == "get_name":
        thoughts.append("Kullanıcı adını sordu")

    else:
        thoughts.append("Bilinmeyen görev")

    return thoughts
