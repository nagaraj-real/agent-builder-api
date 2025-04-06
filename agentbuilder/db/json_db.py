import json
from pathlib import Path
from agentbuilder.helper.json_helper import save_to_json

data_path= str(Path(__file__).parent)+"./../data"

async def get_agents():
    try:
        with open(f"{data_path}/agents.json") as json_file:
                json_data = json.load(json_file)
        return json_data
    except:
         return {}
    
async def get_tools():
    with open(f"{data_path}/tools.json") as json_file:
            json_data = json.load(json_file)
    return json_data

async def get_steps():
    try:
        with open(f"{data_path}/steps.json") as json_file:
                json_data = json.load(json_file)
        return json_data
    except:
         return {}

async def update_agents(agents):
    save_to_json(agents,f"{data_path}/agents")

async def update_tools(tools):
    save_to_json(tools,f"{data_path}/tools")

async def update_agent_steps(steps_to_save):
    save_to_json(steps_to_save,f"{data_path}/steps")


