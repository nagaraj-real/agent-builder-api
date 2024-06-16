
from typing import Sequence
from agentbuilder.tools.weather_tools import weather_clothing_tool,temperature_tool,temperature_sensor_tool
from agentbuilder.tools.sum_tool import sum_tool
from agentbuilder.tools.greeting_tool import greeting_tool
from agentbuilder.tools.git_pull_request_tool import git_pull_request_diff_tool
from agentbuilder.tools.direct_answer_tool import directly_answer_tool
from agentbuilder.tools.repl_tool import repl_tool
from langchain.tools import BaseTool
from agentbuilder.tools.json_tool_kit import json_tools
from agentbuilder.tools.interview_tools.interview_toolkit import interview_tools

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
    
    return  [
            sum_tool,greeting_tool,
            weather_clothing_tool,
            temperature_tool,
            temperature_sensor_tool,
            directly_answer_tool,
            git_pull_request_diff_tool,
            repl_tool,
            ] + interview_tools+get_vectordb_tools()+ get_websearch_tools() + json_tools




