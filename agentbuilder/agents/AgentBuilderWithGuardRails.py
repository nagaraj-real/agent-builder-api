from guardrails import Validator, register_validator
from agentbuilder.agents.BaseAgentBuilder import BaseAgentBuilder
from langchain.output_parsers import GuardrailsOutputParser
from langchain.prompts import PromptTemplate
from guardrails.hub import ValidRange
from langchain_core.runnables import Runnable
import json

@register_validator(name="validate-patient-age", data_type="integer")
class ValidatePatientAge(Validator):
    def validate(self,*args,**kwargs):
        print(args)
        return ValidRange(min=0, max=50,on_fail="exception").validate(*args,**kwargs)
        
rail_spec = """
<rail version="0.1">

<instructions>
You are a helpful assistant only capable of communicating with valid JSON, and no other text.
</instructions>

<output>
    <object name="patient_info">
        <string name="gender" description="Patient's gender" />
        <integer name="age" format="validate-patient-age"/>
        <string name="symptoms" description="Symptoms that the patient is currently experiencing" />
    </object>
</output>

<prompt>

Previous conversation:
{chat_history}

Given the following doctor's notes about a patient, please extract a dictionary that contains the patient's information.

${input}

${gr.complete_json_suffix_v2}

(reminder to respond in a JSON blob no matter what)
</prompt>
</rail>
"""


class AgentBuilderWithGuardRails(BaseAgentBuilder):
    
    output_parser = GuardrailsOutputParser.from_rail_string(rail_spec)

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
            | self.builder_params.chat_llm
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
                print(payload)
                if payload.validation_passed:
                    output="```json\n"+json.dumps(payload.validated_output)+"\n```"
                else:
                    output="Validation failed"
                yield {"output": output}
        return gen()