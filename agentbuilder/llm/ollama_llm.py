from agentbuilder.helper.env_helper import get_ollama_url
from agentbuilder.logger import uvicorn_logger as logger
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain_community.chat_models.ollama import ChatOllama

ollama_url= get_ollama_url()

def ollama_functions_chat(*args,**kwargs):
    model= kwargs.get("model")
    model = "llama3" if model is None else model
    logger.info(f"using model {model}")
    kwargs.update({"model":model,"format":"json","base_url": ollama_url})
    llm = OllamaFunctions(*args,**kwargs)
    return llm


def ollama_chat(*args,**kwargs):
    model= kwargs.get("model")
    model = "llama3" if model is None else model
    logger.info(f"using model {model}")
    kwargs.update({"model":model,"base_url": ollama_url})
    llm = ChatOllama(*args,**kwargs)
    return llm

