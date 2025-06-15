
from typing import Sequence
from agentbuilder.mcp import  MCPClient, get_mcp_client
from agentbuilder.tools.weather_tools import weather_clothing_tool,temperature_tool,temperature_sensor_tool
from agentbuilder.tools.greeting_tool import greeting_tool
from agentbuilder.tools.direct_answer_tool import directly_answer_tool
from langchain.tools import BaseTool


all_tools=None

def get_vectordb_tools():
    try:
        from agentbuilder.tools.vector_store_search_tool import vectorstore_search
        return [vectorstore_search]
    except:
        return []
    
def get_websearch_tools():
    try:
        from agentbuilder.tools.web_search_tool import internet_search
        return [internet_search]
    except:
        return []


def get_all_tools()->Sequence[BaseTool]:
    global all_tools
    mcp_tools=[]
    mcp_client:MCPClient = get_mcp_client()
    if mcp_client:
        mcp_tools= mcp_client.mcp_tools
    all_tools=[ 
            greeting_tool,
            weather_clothing_tool,
            temperature_tool,
            temperature_sensor_tool,
            directly_answer_tool,
            ] + mcp_tools
    return all_tools





