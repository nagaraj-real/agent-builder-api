from pathlib import Path
from agentbuilder.agents.BaseAgentBuilder import BaseAgentBuilder
from langchain_core.runnables import Runnable
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
from langchain_core.output_parsers import StrOutputParser


config = RailsConfig.from_path(str(Path(__file__).parent)+"./config")

class AgentBuilderWithNemoGuardRails(BaseAgentBuilder):
    guardrails = None 

    def __init__(self,params):
        super().__init__(params=params)
        self.guardrails = RunnableRails(config,llm=self.builder_params.chat_llm,tools=self.builder_params.tools)
    
    def create_agent(self) -> Runnable:
        prompt = self.create_prompt()
        agent = (
             prompt
            | (self.guardrails | self.builder_params.chat_llm)
            | StrOutputParser()
        )
        return agent

    
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