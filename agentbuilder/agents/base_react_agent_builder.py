from typing import Any
from langgraph.prebuilt import create_react_agent
from agentbuilder.agents.params import AgentBuilderParams
from agentbuilder.agents.prompt_helper import get_json_agent_prompt,get_default_agent_prompt,get_react_agent_prompt,get_structured_agent_prompt
from langchain.agents import AgentExecutor
from agentbuilder.llm import chat_llm as default_llm
from langchain_core.messages import AIMessage,ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

class BaseReactAgentBuilder:

    chat_llm=None
    # checkpointer = InMemorySaver()
    # config = {"configurable": {"thread_id": "1"}}
    def __init__(self,params:AgentBuilderParams):
        self.builder_params=params
        self.chat_llm = self.builder_params.chat_llm or default_llm

    def compile(self):
        agent = create_react_agent(model=self.chat_llm,tools=self.builder_params.tools)
        return agent
    
    def input_parser(self,params):
        preamble = self.builder_params.preamble
        input = params["input"]
        chat_history= params["chat_history"]
        prompt = get_default_agent_prompt(preamble)
        messages = prompt.format_messages(input=input,chat_history=chat_history)
        return {"messages":messages}
    
    def get_intermediate_steps(self):
        return []
    
    def astream(self,params):
        runnable=  self.compile()
        response= runnable.astream(self.input_parser(params),stream_mode="updates")
        async def gen():
            async for output in response:
                for _, value in output.items():
                    output_dict= self.message_output_parser(value)
                    if(output_dict):
                        yield output_dict
            yield {"intermediate_steps": self.get_intermediate_steps()}
        return gen()
    
    def message_output_parser(self,messages_dict:dict):
         if "messages" in messages_dict:
            messages = messages_dict['messages']
            if messages and isinstance(messages[-1],AIMessage):
                return {"output":messages[-1].content}

    async def ainvoke(self,params):
        runnable=  self.compile()
        response = await runnable.ainvoke(self.input_parser(params))
        messages_dict = response
        parsed_response = self.message_output_parser(messages_dict)
        parsed_response["intermediate_steps"] = self.get_intermediate_steps()
        return parsed_response
        
    def create_prompt(self):
        preamble= self.builder_params.preamble
        return get_react_agent_prompt(preamble)

