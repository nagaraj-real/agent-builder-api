from langchain_core.messages import AIMessage,HumanMessage
from agentbuilder.chat import chat


def get_agent_ui(agent_name:str):
    async def interview_agent_ui(message, history):
        chat_history=[]
        for human, ai in history:
            chat_history.append(HumanMessage(content=human))
            chat_history.append(AIMessage(content=ai))
        response = await chat(message,chat_history,agent_name)
        return response
    return interview_agent_ui