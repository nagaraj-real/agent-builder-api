from langchain_core.tools import StructuredTool
from pydantic.v1 import BaseModel, Field
from agentbuilder.agents.interview.data import interview_state

def save_rating(correct_answer:str,rating:int|str,explanation:str,question_number:int|str) -> str|None:
    """
    Saves the correct answer along with rating and explanation of the user answer for each question
    """
    try:
        interview_state.update_rating_explanation(rating,explanation,question_num=question_number,correct_answer=correct_answer)
        return "saved"
    except Exception as ex:
        return "save failed"

class SaveRatingInputs(BaseModel):
    correct_answer:str = Field(description="Expected correct answer for the question")
    rating:int|str = Field(description="Rating for the answer between 1 to 10")
    explanation:str = Field(description="Rating explanation")
    question_number:int|str = Field(description="question number")

save_rating_tool= StructuredTool.from_function(
        func=save_rating,
        name="save_rating_tool",
        description="Saves the correct answer along with rating and explanation of the user answer for each question",
        args_schema=SaveRatingInputs
    )
