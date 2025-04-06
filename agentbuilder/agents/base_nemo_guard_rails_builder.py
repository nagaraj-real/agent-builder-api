from agentbuilder.agents.base_agent_builder import BaseAgentBuilder
from langchain_core.runnables import Runnable
from nemoguardrails import RailsConfig
from langchain_core.output_parsers import StrOutputParser

class BaseNemoGuardRailsBuilder(BaseAgentBuilder):
    guardrails = None 
    config:RailsConfig = None
    
    def __init__(self,params):
        super().__init__(params=params)

    def create_agent(self) -> Runnable:
        prompt = self.create_prompt()
        agent = (
             prompt
            | self.guardrails
            | StrOutputParser()
        )
        return agent

    def input_parser(self,params):
        return {"input": params["input"],"chat_history": [] }
    
    async def ainvoke(self,params):
        runnable=  self.create_agent()
        response= await runnable.ainvoke(self.input_parser(params))
        return {"output": response}
    
    def astream(self,params):
        runnable=  self.create_agent()
        response= runnable.astream(self.input_parser(params))
        async def gen():
            async for payload in response:
                yield {"output": str(payload)}
        return gen()