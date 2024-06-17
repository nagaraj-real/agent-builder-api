

import os
from agentbuilder.logger import uvicorn_logger as logger

def nvidia_chat(*args,**kwargs):
    from langchain_nvidia_ai_endpoints import ChatNVIDIA
    api_key = os.environ['NVIDIA_API_KEY']
    model= kwargs.get("model")
    model = "meta/llama3-70b-instruct" if model is None else model
    logger.info(f"using model {model}")
    kwargs.update({"api_key":api_key,"model_name": model})
    llm = ChatNVIDIA(base_url="https://integrate.api.nvidia.com/v1", model=model,temperature=0.5,
    top_p=1,
    max_tokens=1024)
    return llm


def nvidia_embed(*args,**kwargs):
    from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings
    api_key = os.environ['NVIDIA_API_KEY']
    model= kwargs.get("model")
    model = "NV-Embed-QA" if model is None else model
    logger.info(f"using model {model}")
    kwargs.update({"api_key":api_key,"model_name": model})
    llm = NVIDIAEmbeddings(base_url="https://integrate.api.nvidia.com/v1",model=model)
    return llm
