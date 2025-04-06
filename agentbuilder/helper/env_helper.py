import os


def get_mongodb_url():
    try:
        url = os.environ["MONGODB_URL"]
        return url
    except:
        return None
    
def get_ollama_url():
    try:
        url = os.environ["OLLAMA_URL"]
        return url
    except:
        return "http://localhost:11434"
    

def get_log_level():
    try:
        return os.environ["LOG_LEVEL"] or "info"
    except:
        return "info"
    

def get_default_agent_type():
    try:
        return os.environ["DEFAULT_AGENT_TYPE"] or "tool_calling"
    except:
        return "tool_calling"
    
    