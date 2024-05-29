from agentbuilder.logger import uvicorn_logger as logger
import os

def cohere_chat(*args,**kwargs):
    from langchain_cohere import ChatCohere
    api_key = os.environ['COHERE_API_KEY']
    model= kwargs.get("model")
    model = "command" if model is None else model
    logger.info(f"using model {model}")
    kwargs.update({"cohere_api_key":api_key,"model":model})
    llm= ChatCohere(*args,**kwargs)
    return llm

def cohere_react_agent(*args,**kwargs):
    from langchain_cohere import create_cohere_react_agent
    return create_cohere_react_agent(*args,**kwargs)

def cohere_embed(*args,**kwargs):
    from langchain_cohere import CohereEmbeddings
    api_key = os.environ['COHERE_API_KEY']
    model= kwargs.get("model")
    model = "embed-english-v2.0" if model is None else model
    logger.info(f"using embed model {model}")
    kwargs.update({"cohere_api_key":api_key,"model":model})
    return CohereEmbeddings(*args,**kwargs)
