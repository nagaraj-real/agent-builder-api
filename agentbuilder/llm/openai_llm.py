import os
from agentbuilder.logger import uvicorn_logger as logger


def openai_chat(*args,**kwargs):
    from langchain_openai import ChatOpenAI
    api_key = os.environ['OPENAI_API_KEY']
    model= kwargs.get("model")
    model = "gpt-3.5-turbo" if model is None else model
    logger.info(f"using model {model}")
    kwargs.update({"openai_api_key":api_key,"model":model})
    llm= ChatOpenAI(*args,**kwargs)
    return llm

def openai_embed(*args,**kwargs):
    from langchain_openai import OpenAIEmbeddings
    api_key = os.environ['OPENAI_API_KEY']
    model= kwargs.get("model")
    model = "text-embedding-ada-002" if model is None else model
    logger.info(f"using embed model {model}")
    kwargs.update({"openai_api_key":api_key,"model":model})
    return OpenAIEmbeddings(*args,**kwargs)