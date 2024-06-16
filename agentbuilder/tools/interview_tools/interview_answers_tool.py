from agentbuilder.agents.interview_agent.data import interview_state
from agentbuilder.agents.interview_agent.data.InterviewStateModel import QuestionAnswer
from langchain_core.tools import StructuredTool

async def interview_answers() -> list[QuestionAnswer]:
    """
    Fetches the list of questions and answers provided during the interview.
    """
    try:
        question_answers = interview_state.get_by_key("question_answers")
        return question_answers
    except Exception as ex:
        return []
    
interview_answers_tool= StructuredTool.from_function(
        coroutine=interview_answers,
        name="interview_answers_tool",
        description="Fetches the list of questions and answers provided during the interview.",
    )