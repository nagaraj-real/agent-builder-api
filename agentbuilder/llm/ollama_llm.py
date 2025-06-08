from agentbuilder.helper.env_helper import get_ollama_url
from agentbuilder.logger import uvicorn_logger as logger


ollama_url= get_ollama_url()

def ollama_chat(*args,**kwargs):
    from langchain_ollama import ChatOllama
    model= kwargs.get("model")
    model = "llama3" if model is None else model
    logger.info(f"using model {model}")
    kwargs.update({"model":model,"base_url": ollama_url})
    llm = ChatOllama(*args,**kwargs)
    return llm

