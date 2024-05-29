from agentbuilder.logger import uvicorn_logger as logger
import os

def gemini_chat(*args,**kwargs):
    from langchain_google_genai import ChatGoogleGenerativeAI
    api_key = os.environ['GOOGLE_API_KEY']
    model= kwargs.get("model")
    model = "gemini-1.5-pro-latest" if model is None else model
    logger.info(f"using model {model}")
    kwargs.update({"google_api_key":api_key,"model": model})
    llm= ChatGoogleGenerativeAI(*args,**kwargs)
    return llm

def gemini_embed(*args,**kwargs):
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    model= kwargs.get("model")
    model = "models/embedding-001" if model is None else model
    logger.info(f"using embed model {model}")
    api_key = os.environ['GOOGLE_API_KEY']
    kwargs.update({"google_api_key":api_key,"model": model})
    return GoogleGenerativeAIEmbeddings(*args,**kwargs)