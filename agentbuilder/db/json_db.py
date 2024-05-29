import json
from agentbuilder.helper.json_helper import save_to_json

async def get_agents():
    try:
        with open("agentbuilder/data/agents.json") as json_file:
                json_data = json.load(json_file)
        return json_data
    except:
         return {}
    
async def get_tools():
    with open("agentbuilder/data/tools.json") as json_file:
            json_data = json.load(json_file)
    return json_data

async def get_steps():
    try:
        with open("agentbuilder/data/steps.json") as json_file:
                json_data = json.load(json_file)
        return json_data
    except:
         return {}

async def update_agents(agents):
    save_to_json(agents,"agentbuilder/data/agents")

async def update_tools(tools):
    save_to_json(tools,"agentbuilder/data/tools")

async def update_agent_steps(steps_to_save):
    save_to_json(steps_to_save,"agentbuilder/data/steps")


