from langchain_core.tools import StructuredTool
from pydantic.v1 import BaseModel, Field
from agentbuilder.agents.interview_agent.data import interview_state

def save_evaluation(markdown_output:str) -> dict|None:
    """
    Saves final evaluation report in markdown format
    """
    try:
        interview_state.get_model().evaluation_output = markdown_output
        return interview_state.get()
    except Exception as ex:
        return None

class SaveEvaluationInputs(BaseModel):
    markdown_output:str = Field(description="Evaluation report in markdown format")

save_evaluation_tool= StructuredTool.from_function(
        func=save_evaluation,
        name="save_evaluation_tool",
        description="Saves final evaluation report in markdown format",
        args_schema=SaveEvaluationInputs
    )