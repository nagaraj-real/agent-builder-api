from typing import List
from nemoguardrails.actions import action
from agentbuilder.agents.interview_agent.data import interview_state


@action(name="UpdateInterviewStateAction", execute_async=True)
async def update_interview_state_action(
    new_data:dict
) -> dict:
    try:
        interview_state.update(new_data)
        return interview_state.get()
    except Exception as ex:
        print(ex)
        return interview_state.get()
    

@action(name="UpdateInterviewQuestionsAction", execute_async=True)
async def update_interview_questions_action(
    question_answer:dict
) -> dict:
    try:
        question_num:int = int(question_answer["question_num"])
        questions_answers:list[dict] = interview_state.get_by_key("question_answers")
        if len(questions_answers) < question_num:
            questions_answers.insert(question_num-1,question_answer)
        else:
            questions_answers[question_num-1].update(question_answer)
        interview_state.update({"question_answers":questions_answers})
        return interview_state.get()
    except Exception as ex:
        print(ex)
        return interview_state.get()
    
@action(name="GetInterviewQuestionsAction", execute_async=True)
async def get_interview_questions_action() -> dict:
    try:
        response= "\n"
        questions_answers:list[dict] = interview_state.get_by_key("question_answers")
        for questions_answer in questions_answers:
            response+=f"Question:  {questions_answer["question"]}\n"
            response+=f"Answer: {questions_answer["answer"]}\n"
        return response
    except Exception as ex:
        print(ex)
        return ""
    
@action(name="GetInterviewStateAction", execute_async=True)
async def get_interview_state_action(
    key:str
) -> str|None:
    try:
        return interview_state.get_by_key(key)
    except Exception as ex:
        print(ex)
        return None
    
@action(name="ClearInterviewStateAction", execute_async=True)
async def clear_interview_state() -> dict|None:
    try:
        return interview_state.reset()
    except Exception as ex:
        print(ex)
        return None
    
@action(name="BotExpressedRatingAction", execute_async=True)
async def bot_expressed_ratingAction(
    output:str=""
) -> str|None:
    try:
        return output
    except Exception as ex:
        print(ex)
        return ""
    
@action(name="UpdateRatingAction", execute_async=True)
async def update_rating_action(
    rating_list:list=[]
) -> str|None:
    try:
        for idx, x in enumerate(rating_list):
            await update_interview_questions_action({"question_num":idx+1,"rating":x})
    except Exception as ex:
        print(ex)
        return ""
    


