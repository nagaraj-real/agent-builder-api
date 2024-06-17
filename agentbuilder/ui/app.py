from dotenv import load_dotenv
import gradio as gr
from agentbuilder.llm import load_chat_llm
from agentbuilder.ui.chat_ui import chat_with_agent
from agentbuilder.db import pesist_db

from agentbuilder.agents.interview_agent.data import interview_state

load_dotenv(override=True)
load_chat_llm()

state = interview_state.get()

with gr.Blocks() as chatdemo:
    chatbot = gr.Chatbot(scale=1, height=600)
    msg = gr.Textbox(label="Message",placeholder="Enter your message here",interactive=True)
    agent = gr.Dropdown(label="Select Agent", choices=["default_agent"], value="default_agent",interactive=True)
    code = gr.Code(language='javascript',interactive=True)
    submit_code = gr.Button(value="Submit")
    clear = gr.ClearButton([msg, chatbot])

    async def code_response(message:str,value:str, chat_history:list,agent:str):
        text_value= message or ""
        human_message=text_value + value
        bot_message = await chat_with_agent(human_message, chat_history,agent)
        chat_history.append((human_message, bot_message))
        return "","", chat_history

    async def update_on_load():
        agents= await pesist_db.get_agents()
        agent_list = list(agents.keys())
        return gr.update(choices=agent_list)
    
    msg.submit(code_response, [msg,code,chatbot,agent], [msg,code, chatbot])
    submit_code.click(code_response,[msg,code,chatbot,agent],[code,code, chatbot])
    
    chatdemo.load(fn=update_on_load, outputs=agent)

with gr.Blocks() as optionsdemo:
    with gr.Row() as row:
        with gr.Column():
            programming_language = gr.Dropdown(interactive=True,label="Programming Language",choices=state["suggested_skills"],allow_custom_value=True,value=state["programming_language"])
            user_confirmed_interview = gr.Checkbox(label="Interview Confirmed",value=state["user_confirmed_interview"])
            questions_count = gr.Number(label="Total number of questions",value=state["questions_count"])
            update_state_button = gr.Button(value="Update State")
            clear_qa = gr.Button(value="Clear Answers")
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
        return model.programming_language ,model.user_confirmed_interview,model.questions_count,model.question_answers
    
    chatbot.change(fn=reload_state,outputs=[programming_language,user_confirmed_interview,questions_count,questions_answers])
    update_state_button.click(update_state,[programming_language,user_confirmed_interview,questions_count],[programming_language,user_confirmed_interview,questions_count])
    clear_qa.click(clear_questions,[],[questions_answers])
    optionsdemo.load(fn=reload_state,outputs=[programming_language,user_confirmed_interview,questions_count,questions_answers])

demo = gr.TabbedInterface([chatdemo, optionsdemo], ["Chat", "Interview State"])


if __name__ == "__main__":
    demo.launch()