chat_history = []
MAX_HISTORY = 20

def add_to_memory(role, message):
    chat_history.append((role, message))

    if len(chat_history) > MAX_HISTORY:
        chat_history.pop(0)