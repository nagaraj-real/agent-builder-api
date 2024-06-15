from dotenv import load_dotenv
import gradio as gr
from agentbuilder.llm import load_chat_llm
from agentbuilder.ui.agent_ui import get_agent_ui
from agentbuilder.db import pesist_db
load_dotenv(override=True)
load_chat_llm()


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(scale=1, height=600)
    msg = gr.Textbox(label="Message",placeholder="Enter your message here")
    agent = gr.Dropdown(label="Select Agent", choices=[], value="default_agent")
    clear = gr.ClearButton([msg, chatbot])

    async def respond(message:str, chat_history:list,agent:str):
        bot_message = await get_agent_ui(agent)(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history

    async def update_on_load():
        agents= await pesist_db.get_agents()
        agent_list = list(agents.keys())
        return gr.update(choices=agent_list)

    msg.submit(respond, [msg, chatbot,agent], [msg, chatbot])
    demo.load(fn=update_on_load, outputs=agent)

if __name__ == "__main__":
    demo.launch()