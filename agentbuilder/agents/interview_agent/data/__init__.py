
from pydantic import BaseModel

class InterviewStateModel(BaseModel):
    programming_language: bool = False
    current_question_number:int = 1
    user_confirmed_interview:bool = False
    question_answers: list=[]


class InterviewState:
    def __init__(self):
        self.interview_state=InterviewStateModel()

    def get(self):
        return self.interview_state.model_dump()

    def update(self,new_data):
        self.interview_state = self.interview_state.model_copy(update=new_data)
        return self.get()
    
    def get_by_key(self,key):
        return self.interview_state.model_dump().get(key)

    def reset(self):
        self.interview_state=InterviewStateModel()
        return self.get()
    
interview_state= InterviewState()