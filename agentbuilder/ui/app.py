import asyncio
from dotenv import load_dotenv
import gradio as gr
from agentbuilder.llm import load_chat_llm
from agentbuilder.main import migrate_to_db
from agentbuilder.ui.chat_ui import chat_with_agent

load_dotenv(override=True)
load_chat_llm()

with gr.Blocks() as chatdemo:
    chatbot = gr.Chatbot(scale=1, height=400,type="tuples")
    msg = gr.Textbox(label="Message",placeholder="Enter your message here",interactive=True)
    agent = gr.Dropdown(label="Select Agent", choices=["weather_clothing_agent"], value="weather_clothing_agent",interactive=True)
    submit = gr.Button(value="Submit",variant="primary")
    clear = gr.ClearButton([msg, chatbot])

    async def code_response(message:str,chat_history:list,agent:str):
        text_value= message or ""
        human_message=text_value
        bot_message = await chat_with_agent(human_message, chat_history,agent)
        chat_history.append((human_message, bot_message))
        return "",chat_history

    
    msg.submit(code_response, [msg,chatbot,agent], [msg, chatbot])
    submit.click(code_response,[msg,chatbot,agent],[msg, chatbot])



demo = gr.TabbedInterface([chatdemo], ["Chat"])

async def migrate_and_launch():
    await migrate_to_db()
    demo.launch()

def launch_ui():
    asyncio.run(migrate_and_launch())

if __name__ == "__main__":
    launch_ui()