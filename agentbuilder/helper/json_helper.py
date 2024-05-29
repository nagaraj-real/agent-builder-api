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

def steps_serializer(messagelog: list[tuple[AgentAction, str]]):
    return [{"tool":action.dict(),"output":output} for action,output in messagelog]