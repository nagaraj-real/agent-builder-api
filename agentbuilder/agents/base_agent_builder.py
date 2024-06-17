from typing import Any
from langchain.agents import create_tool_calling_agent,create_json_chat_agent,create_react_agent,create_structured_chat_agent
from agentbuilder.agents.params import AgentBuilderParams
from agentbuilder.agents.prompt_helper import get_json_agent_prompt,get_default_agent_prompt,get_react_agent_prompt,get_structured_agent_prompt
from langchain.agents import AgentExecutor
from agentbuilder.llm import chat_llm as default_llm
class BaseAgentBuilder:

    chat_llm=None
    def __init__(self,params:AgentBuilderParams):
        self.builder_params=params
        self.chat_llm = self.builder_params.chat_llm or default_llm

    def create_agent(self)-> Any:
        chat_llm= self.chat_llm
        tools= self.builder_params.tools
        preamble= self.builder_params.preamble
        prompt = self.builder_params.prompt or self.create_prompt()
        agent_type= self.builder_params.agent_type
        match agent_type:
            case "tool_calling":
                return create_tool_calling_agent(
                    llm=chat_llm,
                    tools=tools,
                    prompt=prompt,
                ) 
            case "structured":
                prompt = get_structured_agent_prompt(preamble)
                return create_structured_chat_agent(
                    llm=chat_llm,
                    tools=tools,
                    prompt=prompt,
                )
            case "react":
                prompt = get_react_agent_prompt(preamble)
                return create_react_agent(
                    llm=chat_llm,
                    tools=tools,
                    prompt=prompt,
                )
            case "json":
                prompt = get_json_agent_prompt(preamble)
                return create_json_chat_agent(
                    llm=chat_llm,
                    tools=tools,
                    prompt=prompt,
                )
            case _:
                return create_tool_calling_agent(
                    llm=chat_llm,
                    tools=tools,
                    prompt=prompt,
                )
        
    def compile(self):
        agent = self.create_agent()
        tools= self.builder_params.tools
        return AgentExecutor(agent=agent, tools=tools, verbose=True,return_intermediate_steps=True,max_iterations=10,handle_parsing_errors=True)
    
    def input_parser(self,params):
        return {"input": params["input"],"chat_history": params["chat_history"] }
    
    def astream(self,params):
        runnable=  self.compile()
        response= runnable.astream(self.input_parser(params))
        async def gen():
            async for payload in response:
                    yield payload
        return gen()
    
    async def ainvoke(self,params):
        runnable=  self.compile()
        response = await runnable.ainvoke(self.input_parser(params))
        return response
        
    def create_prompt(self):
        agent_type= self.builder_params.agent_type
        preamble= self.builder_params.preamble
        match agent_type:
            case "tool_calling":
                return get_default_agent_prompt(preamble)
            case "structured":
                return get_structured_agent_prompt(preamble)
            case "react":
                return get_react_agent_prompt(preamble)
            case "json":
                return get_json_agent_prompt(preamble)
            case _:
                return get_default_agent_prompt(preamble)

