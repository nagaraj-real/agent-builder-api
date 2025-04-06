from dotenv import load_dotenv
import gradio as gr
from agentbuilder.llm import load_chat_llm
from agentbuilder.ui.chat_ui import chat_with_agent
from agentbuilder.agents.interview.data import interview_state
from agentbuilder.data import data_path


load_dotenv(override=True)
load_chat_llm()

state = interview_state.get()

with gr.Blocks() as chatdemo:
    chatbot = gr.Chatbot(scale=1, height=400)
    msg = gr.Textbox(label="Message",placeholder="Enter your message here",interactive=True)
    agent = gr.Dropdown(label="Select Agent", choices=["interview_agent","rating_agent","interview_question_agent","resume_vector_agent"], value="interview_agent",interactive=False)
    code = gr.Code(language='javascript',interactive=True)
    submit_code = gr.Button(value="Submit",variant="primary")
    clear = gr.ClearButton([msg, chatbot,code])

    async def code_response(message:str,value:str, chat_history:list,agent:str):
        text_value= message or ""
        code_text = "" if value is None or value == "" else f"""\n```javascript\n {value} \n```"""
        human_message=text_value + code_text
        bot_message = await chat_with_agent(human_message, chat_history,agent)
        chat_history.append((human_message, bot_message))
        return "","", chat_history

    
    msg.submit(code_response, [msg,code,chatbot,agent], [msg,code, chatbot])
    submit_code.click(code_response,[msg,code,chatbot,agent],[msg,code, chatbot])
    

with gr.Blocks() as optionsdemo:
    with gr.Row() as row:
        with gr.Column():
            programming_language = gr.Dropdown(interactive=True,label="Programming Language",choices=state["suggested_skills"],allow_custom_value=True,value=state["programming_language"])
            user_confirmed_interview = gr.Checkbox(label="Interview Confirmed",value=state["user_confirmed_interview"])
            questions_count = gr.Number(label="Total number of questions",value=state["questions_count"])
            update_state_button = gr.Button(value="Update State",variant="primary")
            clear_qa = gr.Button(value="Clear Answers")
            reset_state = gr.Button(value="Reset State")
        with gr.Column():
            questions_answers = gr.JSON(label="Question and Answers",value=state["question_answers"],)
    
    def update_state(programming_language:str,user_confirmed_interview:bool, questions_count:int):
        model= interview_state.get_model()
        model.programming_language = programming_language
        model.user_confirmed_interview=user_confirmed_interview
        model.questions_count=questions_count
        return model.programming_language ,model.user_confirmed_interview,model.questions_count
    
    def clear_questions():
        model= interview_state.get_model()
        model.question_answers=[]
        return model.question_answers

    def reload_state():
        model= interview_state.get_model()
        return gr.update(value=model.programming_language,choices=model.suggested_skills) ,model.user_confirmed_interview,model.questions_count,model.question_answers
    
    def clear_state():
        interview_state.reset()
        return reload_state()
    
    chatbot.change(fn=reload_state,outputs=[programming_language,user_confirmed_interview,questions_count,questions_answers])
    update_state_button.click(update_state,[programming_language,user_confirmed_interview,questions_count],[programming_language,user_confirmed_interview,questions_count])
    reset_state.click(clear_state,outputs=[programming_language,user_confirmed_interview,questions_count,questions_answers])
    clear_qa.click(clear_questions,[],[questions_answers])
    optionsdemo.load(fn=reload_state,outputs=[programming_language,user_confirmed_interview,questions_count,questions_answers])

def read_resume_file(file):
    with open(file.name, "r") as f:
        content = f.read()
    return content

    
def read_job_file(file):
    with open(file.name, "r") as f:
        content = f.read()
    return content
        
    
with gr.Blocks() as documents:
    resume = gr.Interface(
        fn=read_resume_file,        
        inputs=gr.File(label="Resume",show_label=True,file_types=["text"],file_count="single",scale=1),   
        outputs=gr.TextArea(label="Resume",placeholder="Resume Content",interactive=True),
    )

    job_description = gr.Interface(
        fn=read_job_file,        
        inputs=gr.File(label="Job description",show_label=True,file_types=["text"],file_count="single",scale=1),   
        outputs=gr.TextArea(label="Job Description",placeholder="Job description",interactive=True)  
    )
    def load_resume_job():
        with open(f"{data_path}/resume.txt", "r") as f:
            resume = f.read()
        with open(f"{data_path}/job_description.txt", "r") as f:
            job = f.read()
        return resume,job
    
    def save_docs(resume,job):
        with open(f"{data_path}/resume.txt", "w") as f:
            f.write(resume)
        with open(f"{data_path}/job_description.txt", "w") as f:
            f.write(job)
        interview_state.get_model().suggested_skills=[]
    
    submit_docs = gr.Button(value="Save",variant="primary")
        
    submit_docs.click(save_docs,resume.output_components+job_description.output_components,[])
    documents.load(fn=load_resume_job,outputs=resume.output_components+job_description.output_components)


demo = gr.TabbedInterface([chatdemo, optionsdemo,documents], ["Chat", "Interview State","Documents"])


if __name__ == "__main__":
    demo.launch()