import os
from agentbuilder.logger import uvicorn_logger as logger


def together_chat(*args,**kwargs):
    from langchain_together import ChatTogether
    model= kwargs.get("model")
    api_key = os.environ['TOGETHER_AI_API_KEY']
    model = "llama3" if model is None else model
    logger.info(f"using model {model}")
    kwargs.update({"api_key":api_key,"model": model})
    llm = ChatTogether(*args,**kwargs)
    return llm

