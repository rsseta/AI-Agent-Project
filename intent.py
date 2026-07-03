# intent.py

intents = {
    "merhaba": "greeting",
    "hesapla": "math",
    "saat": "time",
    "adım neydi": "get_name",
    "adım": "save_name",
    "kaç mesaj": "memory_count",
    "son mesaj": "last_message",
    "geçmiş": "intent_search",
    "tekrar": "repeat",
    "sonucu kaydet": "save_result",
    "sonucu göster": "show_result",
    "olarak kaydet": "variable",
    "araştır": "research",
    "ara": "search_memory",
    "değişkenler": "show_variables",
    "karesi": "square",
    "çık": "exit",
}

#intent detection
def detect_intent(msg):

    msg = msg.lower()
    for intent, task in intents.items():
        if msg.startswith(intent):
            return task

    for intent, task in intents.items():
        if intent in msg:
            return task
    if "topla" in msg:
        return "adding"

    return "unknown"