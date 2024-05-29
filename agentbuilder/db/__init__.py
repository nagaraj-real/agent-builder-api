from typing import Literal, Sequence
import uuid
from langchain.tools import BaseTool
from langchain_core.agents import AgentAction
from agentbuilder.db import json_db
from agentbuilder.helper.env_helper import get_mongodb_url
from agentbuilder.helper.json_helper import agent_serializer, steps_serializer, tools_serializer
from agentbuilder.agents.params import AgentParams
from agentbuilder.types import ToolData

class Database:

    db_type:Literal["jsondb","mongodb"]="jsondb"
    code_agents={}
    def __init__(self,db_type:Literal["jsondb","mongodb"]):
        self.db_type = db_type or "jsondb"
        self.db_mod= self.__get_db_mod()

    def __get_db_mod(self):
        match self.db_type:
            case "mongodb":
                from agentbuilder.db import mongo_db
                return mongo_db
            case _:
                return json_db


    async def get_agents(self)->dict[str,dict]:
        return await self.db_mod.get_agents()

    async def get_steps(self)->dict[str,dict]:
        return await self.db_mod.get_steps()

    async def get_tools(self)->dict[str,ToolData]:
         return await self.db_mod.get_tools()


    async def update_agents(self,agents:dict|None=None):
        agents_to_save= await self.__extract_agents(agents)
        await self.db_mod.update_agents(agents_to_save)

    async def update_tools(self,tools:Sequence[BaseTool]):
        tools_to_save= tools_serializer(tools)
        await self.db_mod.update_tools(tools_to_save)
        

    async def update_agent_steps(self,query,output,agent_name,messagelog: list[tuple[AgentAction, str]]):
        steps_to_save= await self.__extract_agent_steps(query,output,agent_name,messagelog)
        return await self.db_mod.update_agent_steps(steps_to_save)

    async def __extract_agent_steps(self,query,output,agent_name,messagelog: list[tuple[AgentAction, str]]):
        previous_steps= await self.get_steps()
        new_id=str(uuid.uuid1())
        key= f'({query},{agent_name},{new_id})'
        steps_to_save= {key:{"query":query,"id":str(uuid.uuid1()),"agent_name":agent_name,"output":output,"steps":steps_serializer(messagelog)}}
        steps_to_save = steps_to_save if previous_steps is None else {**steps_to_save,**previous_steps}
        return steps_to_save
    
    async def __extract_agents(self,new_agents:dict|None=None):
        db_agents= await self.get_agents()
        if new_agents is not None:
            new_agents = agent_serializer(new_agents)
            all_agents = {**new_agents,**self.code_agents}
        else:
            all_agents = {**db_agents,**self.code_agents}
        return all_agents
    
    def set_code_agents(self,code_agents:dict[str, AgentParams]):
        self.code_agents=agent_serializer(code_agents)
        

mongodb_url= get_mongodb_url()
pesist_db= Database("jsondb") if mongodb_url is None else Database("mongodb")