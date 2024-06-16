from dotenv import load_dotenv
import gradio as gr
from agentbuilder.llm import load_chat_llm
from agentbuilder.ui.agent_ui import get_agent_ui
from agentbuilder.db import pesist_db
load_dotenv(override=True)
load_chat_llm()


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(scale=1, height=600)
    msg = gr.Textbox(label="Message",placeholder="Enter your message here",interactive=True)
    agent = gr.Dropdown(label="Select Agent", choices=["default_agent"], value="default_agent",interactive=True)
    code = gr.Code(language='javascript',interactive=True)
    submit_code = gr.Button(value="Submit Code")
    clear = gr.ClearButton([msg, chatbot])

    
    async def code_response(message:str,value:str, chat_history:list,agent:str):
        text_value= message or ""
        human_message=text_value + value
        bot_message = await get_agent_ui(agent)(human_message, chat_history)
        chat_history.append((human_message, bot_message))
        return "","", chat_history

    async def update_on_load():
        agents= await pesist_db.get_agents()
        agent_list = list(agents.keys())
        return gr.update(choices=agent_list)

    msg.submit(code_response, [msg,code,chatbot,agent], [msg,code, chatbot])
    submit_code.click(code_response,[msg,code,chatbot,agent],[code,code, chatbot])
    demo.load(fn=update_on_load, outputs=agent)

if __name__ == "__main__":
    demo.launch()