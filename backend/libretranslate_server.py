# LibreTranslate removed — translation now handled by Ollama (TinyLLaMA)
# This file is kept to avoid import errors during transition

def start_libretranslate():
    print("LibreTranslate disabled. Using Ollama for translation.")
    return None

def is_server_running():
    return True  # Always return True so app.py skips the start attempt