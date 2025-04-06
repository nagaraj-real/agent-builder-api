from langchain_core.messages import AIMessage,HumanMessage
from agentbuilder.chat import chat


async def chat_with_agent(message, history,agent_name):
    chat_history=[]
    for human, ai in history:
        chat_history.append(HumanMessage(content=human))
        chat_history.append(AIMessage(content=ai))
    response = await chat(message,chat_history,agent_name)
    return response