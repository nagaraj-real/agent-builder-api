from langchain_core.tools import StructuredTool
from pydantic.v1 import BaseModel, Field
from agentbuilder.agents.interview_agent.data import interview_state

async def save_programming_skills(skills_list:list[str]) -> dict|None:
    """
    Saves the interview programming skills
    """
    try:
        interview_state.update({"suggested_skills":skills_list})
        return interview_state
    except Exception as ex:
        print(ex)
        return None

class InterviewSkillsInput(BaseModel):
   skills_list: list[str] = Field(description="programming skills list")

save_skill_tool= StructuredTool.from_function(
        coroutine=save_programming_skills,
        name="save_interview_skills",
        description="Saves the interview programming skills",
        args_schema=InterviewSkillsInput
    )