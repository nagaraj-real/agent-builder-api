
from agentbuilder.agents.interview_agent.data.InterviewStateModel import InterviewStateModel,QuestionAnswer

class InterviewState:
    def __init__(self):
        self.state=InterviewStateModel()
        
    def get_model(self):
        return self.state

    def get(self):
        return self.state.model_dump(mode="json")

    def update(self,new_data):
        self.state = self.state.model_copy(update=new_data)
        return self.get()
    
    def get_by_key(self,key):
        return self.state.model_dump(mode="json").get(key)

    def reset(self):
        self.state=InterviewStateModel()
        return self.get()
    
    def get_question_answers_as_conversation(self):
        response= "\n"
        questions_answers:list[dict] = interview_state.get_by_key("question_answers")
        for questions_answer in questions_answers:
            response+=f"Question:  {questions_answer["question"]}\n"
            response+=f"Answer: {questions_answer["answer"]}\n"
        return response
    
    def update_rating_explanation(self,rating:int,explanation:str,question_num:int):
        qas= self.state.question_answers
        if(question_num):
            qa= next((x for x in qas if x.question_num == question_num), None)
            if qa:
                qa.rating=rating
                qa.explanation=explanation
        print(interview_state.get())
        return interview_state.get()
    
    
    def add_question_answer(self,question:str,answer:str):
        question_answer = QuestionAnswer()
        question_answer.question=question
        question_answer.answer=answer
        question_answer.question_num = len(self.state.question_answers)+1
        self.state.question_answers.append(question_answer)
        return self.state.question_answers

    
interview_state= InterviewState()