from typing import Any, Dict
from langchain.output_parsers import GuardrailsOutputParser
from guardrails.validators import Validator, register_validator, PassResult, FailResult
from agentbuilder.agents.BaseGuardRailsBuilder import BaseGuardRailsBuilder

@register_validator(name="validate-patient-age", data_type="integer")
class ValidatePatientAge(Validator):
    def validate(self,value: Any,metadata: Dict):
        if(value >=50):
             return FailResult(
                error_message=f"Age {value} is greater than 50",
                fix_value=40,
            ) 
        return PassResult() 
        
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


class DoctorAgentBuilder(BaseGuardRailsBuilder):
    
    def __init__(self,params):
        super().__init__(params=params)
        self.output_parser = GuardrailsOutputParser.from_rail_string(rail_spec)
