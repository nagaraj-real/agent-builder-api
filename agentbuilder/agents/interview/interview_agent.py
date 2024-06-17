from pathlib import Path
from agentbuilder.agents.base_nemo_guard_rails_builder import BaseNemoGuardRailsBuilder
from nemoguardrails import RailsConfig
from langchain_core.runnables import Runnable,RunnableLambda
from langchain_core.messages import AIMessage,HumanMessage
from agentbuilder.agents.interview.RunnableAgentRails import RunnableAgentRails
from agentbuilder.agents.interview.data import interview_state

class InterviewAgentBuilder(BaseNemoGuardRailsBuilder):
    guardrails = None 
    config:RailsConfig = None
    def __init__(self,params):
        super().__init__(params=params)
        self.config=RailsConfig.from_path(str(Path(__file__).parent)+"/config")
        self.chat_llm = self.builder_params.chat_llm
        self.guardrails= RunnableAgentRails(config=self.config,llm=self.chat_llm,verbose=True)

    def create_agent(self) -> Runnable:
            agent = (
                RunnableLambda(lambda x:x)
                | self.transform_prompt
                | (self.guardrails|self.chat_llm)
                | self.output_parser
            )
            return agent
    
    def output_parser(self,params):
         return params["output"]

    async def transform_prompt(self,params):
         convo_history = ""
         for message in params["chat_history"]:
              if isinstance(message,HumanMessage):
                   convo_history+=f"user say '{message.content}' \n"
              if isinstance(message,AIMessage):
                   convo_history+=f"bot say '{message.content}' \n"
         interview_data= interview_state.get()
         return {"context":{"convo_history":convo_history,"interview_data": interview_data},"input":params["input"]}

    def input_parser(self,params):
        chat_history = params["chat_history"]
        return {"input": params["input"],"chat_history": chat_history }
    