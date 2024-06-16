import json
from typing import Sequence
from langchain.tools import BaseTool
from langchain_core.agents import AgentAction

from agentbuilder.agents.params import AgentParams

def save_to_json(data,file_name):
    with open(f'{file_name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def agent_serializer(agents:dict[str,AgentParams]):
     return {agent_key:{"name":params.name,
                        "agent_type":params.agent_type,
                        "source_type":params.source_type,
                        "preamble":params.preamble,
                        "tools":[t.name if isinstance(t,BaseTool) else str(t) for t in params.tools]} for (agent_key,params) in agents.items()}

def tools_serializer(tools: Sequence[BaseTool]):
    return {t.name:{"name":t.name,"description": t.description,"metadata":t.metadata,"params": t.args} for t in tools}

def steps_serializer(messagelog: list[tuple[AgentAction, str]],tools=None):
    def augment_file_path(tool_dict):
        tool_name= tool_dict["tool"]
        if tools and tool_name in tools:
            current_tool= tools[tool_name]
            if current_tool:
                if "metadata" in current_tool and current_tool["metadata"] and "file_path" in current_tool["metadata"]:
                    tool_dict["file_path"]=current_tool["metadata"]["file_path"]
        return tool_dict
    
    return [{"tool":augment_file_path(action.dict()),"output":output} for action,output in messagelog]