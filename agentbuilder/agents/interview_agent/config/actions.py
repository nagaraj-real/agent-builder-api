
from nemoguardrails.actions import action
from agentbuilder.agents.agent_helper import create_llm_agent
from agentbuilder.agents.interview_agent.data import interview_state
from agentbuilder.agents.params import AgentParams
from agentbuilder.helper.env_helper import get_default_agent_type

    
def get_resume_tools():
    try:
        from agentbuilder.tools.resume_search_tool import resume_search
        from agentbuilder.tools.job_description_tool import job_description_tool
        from agentbuilder.tools.save_skill_tool import save_skill_tool
        return [resume_search,job_description_tool,save_skill_tool]
    except Exception as ex:
        print(ex)
        return []

def resume_vector_agent():
    return AgentParams(
            name="resume_vector_agent",
            preamble= """
            You are very powerful code assistant,with access to resume and job description tools.
            """,
            tools=  get_resume_tools(),
            agent_type= get_default_agent_type()
      )

vector_llm_agent = create_llm_agent(resume_vector_agent())


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
    
@action(name="GetInterviewFullStateAction", execute_async=True)
async def get_interview_full_state_action() -> dict|None:
    try:
        return interview_state.get()
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


@action(name="GetInterviewJobSkillsAction", execute_async=True)
async def get_interview_job_skills_action() -> str|None:
    try:
        skills_list= interview_state.get_by_key("suggested_skills")
        if skills_list:
            return ','.join(skills_list)

        prompt="""
        You are a bot that can access candidate's resume and a job description.
        Extract a list of programming languages (max 5) that candidate has to focus on
        to help him secure the job. Try to pick languages that the candidate has least experience.
        Finally save the programming language list.
        """
        await vector_llm_agent.ainvoke({"input":prompt,"chat_history":[]})
        return ','.join(interview_state.get_by_key("suggested_skills"))
    except Exception as ex:
        print(ex)
        return ""
    
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
    


