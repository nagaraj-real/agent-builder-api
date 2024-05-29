from agentbuilder.logger import uvicorn_logger as logger
import os

def anthropic_chat(*args,**kwargs):
    from langchain_anthropic import ChatAnthropic
    api_key = os.environ['ANTHROPIC_API_KEY']
    model= kwargs.get("model")
    model = "claude-3-haiku-20240307" if model is None else model
    logger.info(f"using model {model}")
    kwargs.update({"api_key":api_key,"model_name": model})
    llm= ChatAnthropic(*args,**kwargs)
    return llm

def voyage_embed(*args,**kwargs):
    from langchain_voyageai import VoyageAIEmbeddings
    api_key = os.environ['VOYAGE_API_KEY']
    model= kwargs.get("model")
    model = "voyage-2" if model is None else model
    logger.info(f"using embed model {model}")
    kwargs.update({"voyage_api_key":api_key,"model": model})
    return VoyageAIEmbeddings(*args,**kwargs)