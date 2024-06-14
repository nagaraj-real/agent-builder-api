from pathlib import Path
from agentbuilder.agents.BaseNemoGuardRailsBuilder import BaseNemoGuardRailsBuilder
from nemoguardrails import RailsConfig
from nemoguardrails.integrations.langchain.runnable_rails import RunnableRails
from langchain_core.runnables import Runnable,RunnableLambda
from langchain_core.messages import AIMessage,HumanMessage
from agentbuilder.agents.interview_agent.data import interview_state

class InterviewAgentBuilder(BaseNemoGuardRailsBuilder):
    guardrails = None 
    config:RailsConfig = None
    def __init__(self,params):
        super().__init__(params=params)
        self.config=RailsConfig.from_path(str(Path(__file__).parent)+"./config")
        self.guardrails= RunnableRails(config=self.config,llm=self.builder_params.chat_llm,verbose=True)

    def create_agent(self) -> Runnable:
            agent = (
                RunnableLambda(lambda x:x)
                | self.transform_prompt
                | (self.guardrails|self.builder_params.chat_llm)
                | self.output_parser
            )
            return agent
    
    def output_parser(self,params):
         print(params)
         return params["output"]

    async def transform_prompt(self,params):
         convo_history = ""
         for message in params["chat_history"]:
              if isinstance(message,HumanMessage):
                   convo_history+=f"user say '{message.content}' \n"
              if isinstance(message,AIMessage):
                   convo_history+=f"bot say '{message.content}' \n"
         interview_data= interview_state.get()
         print(interview_data)
         return {"context":{"convo_history":convo_history,"interview_data": interview_data},"input":params["input"]}

    def input_parser(self,params):
        chat_history = params["chat_history"]
        return {"input": params["input"],"chat_history": chat_history }
    