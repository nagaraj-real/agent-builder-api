
from agentbuilder.agents.interview.data.models import InterviewStateModel,QuestionAnswer

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
        questions_answers:list[QuestionAnswer] = self.state.question_answers
        for questions_answer in questions_answers:
            response+=f"Question:  {questions_answer.question}\n"
            response+=f"Answer: {questions_answer.answer}\n"
        return response
    
    def get_evaluation_report(self):
        questions_answers:list[QuestionAnswer] = self.state.question_answers
        response=""
        for qa in questions_answers:
            rating_stars = self.get_rating_stars(qa.rating)
            response+=f"""
            \n### Question {qa.question_num}
            \n**Question**: {qa.question}
            \n**Answer:** 
            \n {qa.answer}
            \n**Rating:** {rating_stars}
            \n**Explanation:** {qa.explanation}
            \n**Expected Answer:** 
            \n {qa.correct_answer}
            \n ---
            """
        self.state.evaluation_output = response
        return response
    
    def get_rating_stars(self,count):
        return "".join(["⭐" for i in list(range(count))])


    def get_question_answer(self,question_num:int):
        qas= self.state.question_answers
        question_number= int(question_num)
        if(question_number):
            qa= next((x for x in qas if x.question_num == question_number), None)
            return qa
        return None
    
    def update_rating_explanation(self,rating:int,explanation:str,question_num:int,correct_answer:str):
        qas= self.state.question_answers
        question_number= int(question_num)
        rating = int(rating)
        if(question_number):
            qa= next((x for x in qas if x.question_num == question_number), None)
            if qa:
                qa.rating=int(rating)
                qa.explanation=explanation
                qa.correct_answer=correct_answer
        return self.get()
    
    
    def add_question_answer(self,question:str,answer:str):
        question_answer = QuestionAnswer()
        question_answer.question=question
        question_answer.answer=answer
        question_answer.question_num = len(self.state.question_answers)+1
        self.state.question_answers.append(question_answer)
        return self.state.question_answers
