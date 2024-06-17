from agentbuilder.logger import uvicorn_logger as logger
from langchain_core.messages import BaseMessage,AIMessage,HumanMessage
from agentbuilder.agents.base_agent_builder import BaseAgentBuilder
from agentbuilder.agents.agent_helper import build_agent
from langchain_core.prompts import ChatPromptTemplate
from agentbuilder.llm import get_chat_llm,get_casual_chat_prompt
from agentbuilder.db import pesist_db as db

async def chat(query:str,chat_history:list[BaseMessage]=[],agent_name=None)->str:
    agent_builder:BaseAgentBuilder|None = await build_agent(agent_name)
    if agent_builder is None:
        return await chat_without_agent(query,chat_history)
    try:
        response = await agent_builder.ainvoke({"input": query,"chat_history": chat_history })
        if("intermediate_steps" in response):
            await db.update_agent_steps(query,response["output"],agent_name,response["intermediate_steps"])
        return response["output"]
    except Exception as exc:
        logger.error(f"Error: {str(exc)}")
        raise exc
    
async def chat_stream(query:str,chat_history:list[BaseMessage]=[],agent_name=None):
    agent_builder:BaseAgentBuilder|None = await build_agent(agent_name)
    if agent_builder is None:
        return await chat_without_agent_stream(query,chat_history)
    try:
        response= agent_builder.astream({"input": query,"chat_history": chat_history })
        async def gen():
            intermediate_steps=[]
            final_output=""
            async for payload in response:
                if("intermediate_steps" in payload):
                    intermediate_steps=payload["intermediate_steps"]
                if "output" in payload:
                    final_output += payload["output"] # type: ignore
                yield payload
            await db.update_agent_steps(query,final_output,agent_name,intermediate_steps)
        return gen()
    except Exception as exc:
        logger.error(f"Error: {str(exc)}")
        raise exc
    
async def chat_without_agent(query:str,chat_history:list[BaseMessage]=[])->str:
    try:
        prompt: ChatPromptTemplate = get_casual_chat_prompt("You are a chatbot that can have a casual chat")
        if not chat_history:
            chat_history.extend(prompt.format_messages(input=query))
        else:
            chat_history.extend([HumanMessage(content=query)])
        response:BaseMessage = await get_chat_llm(casual=True).ainvoke(chat_history)
        return str(response.content)
    except Exception as exc:
        logger.error(f"Error: {str(exc)}")
        raise exc
    
async def chat_without_agent_stream(query:str,chat_history:list[BaseMessage]=[]):
    try:
        prompt: ChatPromptTemplate = get_casual_chat_prompt("You are a chatbot that can have a casual chat")
        if not chat_history:
            chat_history.extend(prompt.format_messages(input=query))
        else:
            chat_history.extend([HumanMessage(content=query)])
        response= get_chat_llm(casual=True).astream(chat_history) # type: ignore
        async def gen():
            async for payload in response: # type: ignore
                if isinstance(payload,BaseMessage):
                    yield {"output":payload.content,"messages":[AIMessage(content=payload.content)]}
        return gen()
    except Exception as exc:
        logger.error(f"Error: {str(exc)}")
        raise exc
    




    
   
    