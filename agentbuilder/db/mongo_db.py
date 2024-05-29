from agentbuilder.logger import uvicorn_logger as logger
import motor.motor_asyncio
from agentbuilder.agents.params import SerializedAgentParams
from agentbuilder.db.db_models.agents_model import AgentModel
from agentbuilder.db.db_models.tool_model import ToolModel
from agentbuilder.helper.env_helper import get_mongodb_url

mongodb_url= get_mongodb_url()
client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
mongo_db = client.get_database("llmdb")
agents_collection = mongo_db.get_collection("agents")
tools_collection = mongo_db.get_collection("tools")
steps_collection = mongo_db.get_collection("steps")


async def get_agents():
    agents={}
    cursor= await agents_collection.find({}).to_list(length=None)
    for document in cursor:
        agents[str(document['name'])] = AgentModel(**document).model_dump(exclude=set(['id']))
    return agents


async def update_agents(agents:dict[str,SerializedAgentParams]):
    await agents_collection.delete_many({})
    result= await agents_collection.insert_many(agents.values())
    logger.debug(f"Inserted {len(result.inserted_ids)}")

async def get_tools():
    tools={}
    cursor= await tools_collection.find({}).to_list(length=None)
    for document in cursor:
        tools[str(document['name'])] = ToolModel(**document).model_dump(exclude=set(['id']))
    return tools

async def update_tools(tools):
    await tools_collection.delete_many({})
    result= await tools_collection.insert_many(tools.values())
    logger.debug(f"Inserted {len(result.inserted_ids)}")

async def get_steps():
    steps={}
    cursor= await steps_collection.find({}).to_list(length=None)
    for document in cursor:
        steps_dict:dict = {**document}
        steps_dict.pop("_id")
        steps[str(document['_id'])] = steps_dict
    return steps

async def update_agent_steps(steps:dict):
    await steps_collection.delete_many({})
    result= await steps_collection.insert_many(steps.values())
    logger.debug(f"Inserted {len(result.inserted_ids)}")
