
from pydantic import BaseModel

class QuestionAnswer(BaseModel):
    question: str=""
    answer:str=""
    question_num: int=0
    rating: int=0
    explanation: str=""

class InterviewStateModel(BaseModel):
    programming_language: str = ""
    current_question:str = ""
    user_confirmed_interview:bool = False
    question_answers: list[QuestionAnswer]=[]
    suggested_skills: list=[]
    questions_count:int = 3
    evaluation_output: str = ""

test_data= InterviewStateModel(
  programming_language="javascript",
  current_question_number= 6,
  user_confirmed_interview=True,
  suggested_skills=["React", "Java"],
  question_answers=[
    {
      "question": "Can you explain the concept of closures in the programming language you are familiar with?",
      "question_num": 1,
      "answer": "closure"
    },
    {
      "question": "Can you explain the difference between pass by value and pass by reference in the programming language you are familiar with?",
      "question_num": 2,
      "answer": "pass by value"
    },
    {
      "question": "Can you explain the concept of polymorphism in the programming language you are familiar with?",
      "question_num": 3,
      "answer": "polymorphism"
    },
    {
      "question": "Can you explain the difference between synchronous and asynchronous programming in the programming language you are familiar with?",
      "question_num": 4,
      "answer": "async"
    },
    {
      "question": "Can you explain the concept of hoisting in the programming language you are familiar with?",
      "question_num": 5,
      "answer": "hoisting"
    }
  ])
