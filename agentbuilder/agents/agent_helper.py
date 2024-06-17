from agentbuilder.logger import uvicorn_logger as logger
from typing import Any, Callable
from langchain.tools import BaseTool
from agentbuilder.agents.base_agent_builder import AgentBuilderParams, BaseAgentBuilder
from agentbuilder.agents.params import AgentParams
from agentbuilder.factory.tool_factory import get_all_tools
from agentbuilder.factory.agent_factory import get_agent_builder
from agentbuilder.factory.agent_factory import get_all_agents


def create_llm_agent(params: AgentParams):
    from agentbuilder.llm import chat_llm
    logger.debug(f"Creating Agent with params: {params}")
    tools= [t for t in extract_tools(params.tools) if t is not None]
    agent_type= params.agent_type
    name= params.name
    agent_builder = get_agent_builder(AgentBuilderParams(name,agent_type,tools,preamble=params.preamble,prompt=params.prompt,chat_llm=chat_llm))
    return agent_builder


async def get_agent(agent_name:str|None):
     all_agents = get_all_agents()
     agent_params = next((x for x in all_agents if x.name == agent_name), None)
     return agent_params


async def build_agent(agent_name:str|None)-> None | BaseAgentBuilder:
     agent_params = await get_agent(agent_name)
     if agent_params is None:
          return None
     return create_llm_agent(agent_params)

def extract_tools(tools:list[BaseTool|str|Callable]):
    if not tools:
         return []
    def get_tool(tool:BaseTool|str|Any)->BaseTool|None:
        if isinstance(tool,str):
            result_tools= [t for t in get_all_tools() if t.name==tool]
            return result_tools[0] if len(result_tools)>0 else None
        else:
            return tool
    return [get_tool(tool) for tool in tools]


    