
from nemoguardrails.actions import action
from agentbuilder.agents.interview_agent.data import interview_state
from agentbuilder.chat import chat

@action(name="UpdateInterviewStateAction", execute_async=True)
async def update_interview_state_action(
    new_data:dict
) -> dict:
    try:
        interview_state.update(new_data)
        return interview_state.get()
    except Exception as ex:
        return interview_state.get()


@action(name="AddInterviewQuestionsAction", execute_async=True)
async def add_interview_questions_action(
    answer:str
) -> dict:
    try:
        question = interview_state.get_model().current_question
        interview_state.add_question_answer(question,answer)
        return interview_state.get_by_key("question_answers")
    except Exception as ex:
        return interview_state.get_by_key("question_answers")
    
@action(name="GetInterviewStateAction", execute_async=True)
async def get_interview_state_action(
    key:str
) -> str|None:
    try:
        return interview_state.get_by_key(key)
    except Exception as ex:
        return None
    
@action(name="GetInterviewFullStateAction", execute_async=True)
async def get_interview_full_state_action() -> dict|None:
    try:
        return interview_state.get()
    except Exception as ex:
        return None
    
@action(name="ClearInterviewStateAction", execute_async=True)
async def clear_interview_state() -> dict|None:
    try:
        return interview_state.reset()
    except Exception as ex:
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
        await chat(prompt,[],"resume_vector_agent")
        return ','.join(interview_state.get_by_key("suggested_skills"))
    except Exception as ex:
        return ""
    
@action(name="BotExpressedQuestionAction", execute_async=True)
async def bot_expressed_question_action(
    output:str=""
) -> str|None:
    try:
        return output
    except Exception as ex:
        return ""

@action(name="InterviewRatingAction", execute_async=True)
async def interview_rating_action() -> str|None:
    try:
        programming_language:str=interview_state.get_by_key("programming_language")

        prompt=f"""
        You are a rating bot that can rate question and answers
        provided by the user in {programming_language} interview.

        Provide a rating for each answer with explanation.
        Remember this interview is for a Lead Programming Developer Role and provide a rating based on that.
        Make sure the answers are accurate and descriptive. Use the following criteria to rate.
        Answer them yourself to compare your answer with the user answers.
        - Assign rating below 5 if the answer is inaccurate.
        - Assign rating above 5 but below 7 if the answer is accurate but not perfect.
        - Assign 8, 9 or 10 only if the answer is perfect.
    
        Follow these steps:
        ## Step 1 
        Fetch question, answers using tools.
        ## Step 2
        Generate a markdown to display the rating and explanation for each question: <<evaluation_markdown_output>>.
        Seperate each Q & A with horizontal line and use proper headings.
        Place question, answer, rating , explanation on seperate lines.
        Use star emojis to convey rating.
        ## Step 3
        Extract the rating,explanation for each question and save each of them using tools.
        ## Step 4
        Save the output in markdown format: <<evaluation_markdown_output>> using save evaluation tool.
        and provide the output as response.
        """
        await chat(prompt,[],agent_name="rating_agent")
        return interview_state.get_model().evaluation_output
    except Exception as ex:
        return ""
    
    


