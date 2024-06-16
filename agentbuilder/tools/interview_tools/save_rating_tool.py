from langchain_core.tools import StructuredTool
from pydantic.v1 import BaseModel, Field
from agentbuilder.agents.interview_agent.data import interview_state

async def save_rating(rating:int,explanation:str,question_number:int) -> dict|None:
    """
    Saves the interview programming skills
    """
    try:
        interview_state.update_rating_explanation(rating,explanation,question_num=question_number)
        return interview_state.get()
    except Exception as ex:
        return None

class SaveRatingInputs(BaseModel):
    rating:int = Field(description="Rating for the answer between 1 to 10")
    explanation:str = Field(description="Rating explanation")
    question_number:str = Field(description="question number")

save_rating_tool= StructuredTool.from_function(
        coroutine=save_rating,
        name="save_rating_tool",
        description="Saves the rating for each question",
        args_schema=SaveRatingInputs
    )
