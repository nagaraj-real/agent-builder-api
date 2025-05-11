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

def normalize_schema(schema, root_schema):
    """
    Recursively resolve all $ref keys within a schema using definitions from root_schema["$defs"].
    - If schema is a flat object with 'type' entries, return as-is.
    - Otherwise, recursively replace all $ref entries with their resolved versions.
    """
    if all(isinstance(v, dict) and 'type' in v for v in schema.values()):
        return schema

    def resolve(obj):
        if isinstance(obj, dict):
            if "$ref" in obj and len(obj) == 1:
                ref:str = obj["$ref"]
                if ref.startswith("#/$defs/"):
                    key = ref.split("/")[-1]
                    return resolve(root_schema.get("$defs", {}).get(key, {}))
                return obj  # leave unresolved if $ref doesn't match
            return {k: resolve(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [resolve(item) for item in obj]
        return obj

    return resolve(schema)

def tools_serializer(tools: Sequence[BaseTool]):
    def get_args(t:BaseTool):
        args=t.args
        return normalize_schema(args,t.args_schema)
    return {t.name:{"name":t.name,"description": t.description,"metadata":t.metadata,"params": get_args(t)} for t in tools}

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