import operator
from typing import Annotated, Literal, TypedDict, Union
from langchain_core.agents import (
    AgentAction,
    AgentFinish,
)
from agentbuilder.agents.base_graph_agent_builder import AgentState, BaseGraphAgentBuilder
from agentbuilder.agents.interview.data import interview_state
from agentbuilder.agents.params import AgentBuilderParams
from langchain.agents import create_structured_chat_agent
from langgraph.graph import StateGraph
from agentbuilder.agents.prompt_helper import get_structured_agent_prompt, get_vector_search_prompt
from langchain_core.messages import BaseMessage
from langchain.agents import AgentExecutor
from langgraph.graph import END, StateGraph
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from agentbuilder.tools.interview_tools.job_description_tool import load_job_retriever
from agentbuilder.tools.interview_tools.resume_search_tool import load_resume_retriever

class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    job_skills: list[str]
    resume_skills: list[str]
    job_summary: str
    suggested_skills:list[str]


class ResumeJobAgentBuilder(BaseGraphAgentBuilder):

    def __init__(self,params:AgentBuilderParams):
        super().__init__(params=params)
        self.chat_llm= self.builder_params.chat_llm
        tools= self.builder_params.tools
        preamble = self.builder_params.preamble
        self.agent= create_structured_chat_agent(llm=self.chat_llm,tools=tools,prompt=get_structured_agent_prompt(preamble))
        

    def initialize_graph(self):
        self.builder.add_node("extract_job_skills", self.extract_job_skills)
        self.builder.add_node("extract_resume_skills", self.extract_resume_skills)
        self.builder.add_node("save_suggested_skills", self.save_suggested_skills)

        self.builder.add_node("save_skills_action", self.execute_tools)
        self.builder.add_edge("save_skills_action", "save_suggested_skills")

        self.builder.add_edge("extract_job_skills","extract_resume_skills")
        self.builder.add_edge("extract_resume_skills","save_suggested_skills")
        self.builder.add_conditional_edges(
        "save_suggested_skills",
        self.should_continue,
            {
            "continue": "save_skills_action",
            "end": END,
            },
        )
        self.builder.set_entry_point("extract_job_skills")

    def execute_tools(self,state):
        agent_output = state["agent_outcome"]
        if len(agent_output['intermediate_steps'])>=1 :
            agent_action = agent_output['intermediate_steps'][0][0]
            output = self.get_agent_executer().invoke(agent_action)
            return {"intermediate_steps": [(agent_action, str(output))]}
        else:
            return {"intermediate_steps":[]}

    def initialize_state(self):
        self.builder= StateGraph(AgentState)

    def should_continue(self,state: AgentState) -> Literal["tools", "__end__"]:
        if state["agent_outcome"]["output"] is not None:
            return "end"
        else:
            return "continue"
        
    def get_agent_executer(self):
        return AgentExecutor(agent=self.agent, 
                             tools=self.builder_params.tools, 
                             verbose=True,
                             max_iterations=3,
                             return_intermediate_steps=True,
                             handle_parsing_errors=True
                             )

    async def ainvoke(self,params):
        runnable=  self.compile()
        response = await runnable.ainvoke(self.input_parser(params))
        return response['agent_outcome']

     
    def input_parser(self,params):
        input = params["input"]
        chat_history= params["chat_history"]
        return {"input":input,"chat_history": chat_history,"question_number":1}
    
    def extract_job_skills(self,state: AgentState):
        prompt = get_vector_search_prompt()
        document_chain = create_stuff_documents_chain(self.chat_llm, prompt)
        job_description_retriever= load_job_retriever()
        retrieval_chain = create_retrieval_chain(job_description_retriever, document_chain)
        response = retrieval_chain.invoke({"input": self.get_extract_job_skills_prompt()})
        summary = retrieval_chain.invoke({"input": """
                                          Summarize the job description in a paragraph.
                                          This summary should include the skills and areas candidate should focus
                                          on his interview preparation.
                                          """})
        interview_state.get_model().job_summary = summary["answer"]
        return {"job_skills": response["answer"],"job_summary":summary["answer"]}
    
    def extract_resume_skills(self,state: AgentState):
        prompt = get_vector_search_prompt()
        document_chain = create_stuff_documents_chain(self.chat_llm, prompt)
        resume_search_retriever = load_resume_retriever()
        retrieval_chain = create_retrieval_chain(resume_search_retriever, document_chain)
        response = retrieval_chain.invoke({"input": self.get_extract_resume_skills_prompt()})
        return {"resume_skills": response["answer"]}
    
    def save_suggested_skills(self,state: AgentState):
        chat_history= state['chat_history']
        response = self.get_agent_executer().invoke({"input":self.get_save_skills_prompt(state),"chat_history":chat_history})
        return {"agent_outcome": response}

    
    def get_extract_job_skills_prompt(self):
        prompt=f"""
            Extract the skills(programming languages) from job description using tools.
            Return the list of programming languages seperated by comma. Do not include any other text.

            Output example: "Java","Ruby","python"
            """
        return prompt
    
    def get_extract_resume_skills_prompt(self):
        prompt=f"""
            Extract the skills(programming languages) from resume using tools.
            Return the list of programming languages seperated by comma. Do not include any other text.

            Output example: "Java","Ruby","python"
            """
        return prompt
    
    def get_save_skills_prompt(self,state:AgentState):
        job_skills= state["job_skills"] 
        resume_skills = state["resume_skills"] 
        prompt=f"""
            # Programming Skills that candidate already have good knowledge:
            {resume_skills}

            # Programming Skills required to be successfull at the Job:
            {job_skills}

            Create a list of suggested programming skills(Maximum 5) the candidate should focus to be successfull on job.

            Save the list of suggested programming languages using tools.
            """
        return prompt
    

    

