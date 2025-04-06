from agentbuilder.agents.base_guard_rails_builder import BaseAgentBuilder
from langchain.output_parsers import GuardrailsOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
import json
        

class BaseGuardRailsBuilder(BaseAgentBuilder):
    
    output_parser:GuardrailsOutputParser = None

    def __init__(self,params):
        super().__init__(params=params)
    
    def create_prompt(self):
        prompt = PromptTemplate(
            template=self.output_parser.guard.prompt.escape(),
            input_variables=self.output_parser.guard.prompt.variable_names,
        )
        return prompt
    
    def create_agent(self) -> Runnable:
        prompt = self.create_prompt()
        agent = (
             prompt
            | self.chat_llm
            | self.output_parser
        )
        return agent
    
    async def ainvoke(self,params):
        runnable=  self.create_agent()
        response= await runnable.ainvoke(self.input_parser(params))
        if response.validation_passed:
            output="```json\n"+json.dumps(response.validated_output)+"\n```"
        else:
            output="Validation failed"
        return {"output": output}
    
    def astream(self,params):
        runnable=  self.create_agent()
        response= runnable.astream(self.input_parser(params))
        async def gen():
            async for payload in response:
                if payload.validation_passed:
                    output="```json\n"+json.dumps(payload.validated_output)+"\n```"
                else:
                    output="Validation failed"
                yield {"output": output}
        return gen()