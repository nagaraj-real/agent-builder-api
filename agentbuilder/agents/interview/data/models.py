
from pydantic import BaseModel

class QuestionAnswer(BaseModel):
    question: str=""
    answer:str=""
    question_num: int=0
    rating: int=0
    explanation: str=""
    correct_answer:str=""

class InterviewStateModel(BaseModel):
    programming_language: str = ""
    current_question:str = ""
    user_confirmed_interview:bool = False
    question_answers: list[QuestionAnswer]=[]
    suggested_skills: list=[]
    questions_count:int = 3
    evaluation_output: str = ""
    job_summary:str=""

test_data= InterviewStateModel(
  programming_language="javascript",
  current_question_number= 6,
  user_confirmed_interview=True,
  suggested_skills=["React", "Java"],
  question_answers=[
    QuestionAnswer(question='Explain the concept of state and props in React and how they differ from each other.', 
                     answer='hi', 
                     question_num=1,
                       rating=0, explanation=''), 
    QuestionAnswer(question="""Write a React component that uses the useState hook to 
                   manage a counter and display the current count on the screen.""", 
                   answer='hi', question_num=2, rating=0, explanation='')])
