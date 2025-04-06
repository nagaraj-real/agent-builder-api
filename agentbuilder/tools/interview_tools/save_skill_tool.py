
from langchain_core.tools import StructuredTool
from pydantic.v1 import BaseModel, Field
from agentbuilder.agents.interview.data import interview_state

def save_programming_skills(skills_list:list[str]) -> dict|None:
    """
    Saves the interview programming skills
    """
    try:
        interview_state.get_model().suggested_skills=skills_list
        return "saved"
    except Exception as ex:
        return "not saved"

class InterviewSkillsInput(BaseModel):
   skills_list: list[str] = Field(description="programming skills list")

save_skill_tool= StructuredTool.from_function(
        func=save_programming_skills,
        name="save_skill_tool",
        description="Saves the interview programming skills",
        args_schema=InterviewSkillsInput
    )