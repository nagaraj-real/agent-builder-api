import os


def get_mongodb_url():
    try:
        url = os.environ["MONGODB_URL"]
        return url
    except:
        return None
    

def get_log_level():
    try:
        return os.environ["LOG_LEVEL"] or "info"
    except:
        return "info"
    