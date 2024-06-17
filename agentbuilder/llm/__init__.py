
from agentbuilder.logger import uvicorn_logger as logger
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.embeddings import Embeddings
from agentbuilder.llm.anthropic_llm import anthropic_chat, voyage_embed
from agentbuilder.llm.gemini_llm import gemini_chat,gemini_embed
from agentbuilder.llm.cohere_llm import cohere_chat,cohere_embed
from agentbuilder.llm.ollama_llm import ollama_chat,ollama_functions_chat
from agentbuilder.llm.openai_llm import openai_chat,openai_embed
from agentbuilder.llm.nvidia_llm import nvidia_chat, nvidia_embed
from langchain.agents import create_tool_calling_agent
import os

chat_llm = None

def get_chat_llm(*args,**Kwargs):
    model_name= os.getenv("MODEL_NAME")
    if model_name is None:
     raise Exception(f"Model not found: {model_name}") 
    (provider,model)=extract_after_slash(model_name)
    is_casual= Kwargs.pop("casual") if Kwargs.get("casual") else False
    default_kwargs ={"model": model}
    default_kwargs.update(Kwargs)
    logger.info(f"using chat provider: {provider}")
    match provider:
        case "ollama":
            return  ollama_chat(*args,**default_kwargs) if is_casual else ollama_functions_chat(*args,**default_kwargs)
        case "cohere":
            return cohere_chat(*args,**default_kwargs)
        case "gemini":
            return gemini_chat(*args,**default_kwargs)
        case "openai":
            return openai_chat(*args,**default_kwargs)
        case "anthropic":
            return anthropic_chat(*args,**default_kwargs)
        case "nvidia":
            return nvidia_chat(*args,**default_kwargs)
        case _:
            raise Exception(f"Model not found: {model}")


def create_agent(*args,**Kwargs):
    return create_tool_calling_agent(*args,**Kwargs)

def get_embed_llm(*args,**Kwargs) -> Embeddings:
    model_name= os.getenv("EMBED_MODEL_NAME")
    if model_name is None:
     raise Exception(f"Model not found: {model_name}") 
    (provider,model)=extract_after_slash(model_name)
    default_kwargs ={"model": model}
    default_kwargs.update(Kwargs)
    logger.info(f"using embed provider: {provider}")
    match provider:
        case "cohere":
            return cohere_embed(*args,**default_kwargs)
        case "gemini":
            return gemini_embed(*args,**default_kwargs)
        case "openai":
            return openai_embed(*args,**default_kwargs)
        case "voyageai":
            return voyage_embed(*args,**default_kwargs)
        case "nvidia":
            return nvidia_embed(*args,**Kwargs) 
        case _:
            raise Exception(f"Embed Model not found: {model}")

def get_casual_chat_prompt(preamble:str|None)->ChatPromptTemplate:
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                preamble,
            ), # type: ignore
            ("user", "{input}"),
        ]
    )
    return prompt

def extract_after_slash(text):
  if "/" in text:
    parts = text.split("/")
    return (parts[0],parts[1])
  else:
    return (text,None)

def load_chat_llm():
    global chat_llm
    try:
        chat_llm = get_chat_llm()
    except Exception as exc:
        logger.error(f"Error: {str(exc)}")