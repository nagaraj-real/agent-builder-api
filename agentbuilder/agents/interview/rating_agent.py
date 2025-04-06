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
from agentbuilder.agents.prompt_helper import get_structured_agent_prompt
from langchain_core.messages import BaseMessage
from langchain.agents import AgentExecutor
from langgraph.graph import END, StateGraph

class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]
    question_number: int


class RatingAgentBuilder(BaseGraphAgentBuilder):

    def __init__(self,params:AgentBuilderParams):
        super().__init__(params=params)
        self.chat_llm = self.builder_params.chat_llm
        tools= self.builder_params.tools
        preamble = self.builder_params.preamble
        self.agent= create_structured_chat_agent(llm=self.chat_llm,tools=tools,prompt=get_structured_agent_prompt(preamble))

    def initialize_graph(self):
        self.builder.add_node("rate_answer", self.rate_answer)
        self.builder.add_node("markdown", self.generate_markdown)
        self.builder.add_node("action", self.execute_tools)
        self.builder.add_edge('action', "rate_answer")
        self.builder.add_edge('markdown', END)
        self.builder.add_conditional_edges(
        "rate_answer",
        self.should_continue,
            {
            "continue": "action",
            "rate_answer": "rate_answer",
            "markdown": "markdown"
            },
        )
        self.builder.set_entry_point("rate_answer")

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
        question_num = state["question_number"]
        qas= interview_state.get_model().question_answers
        if state["agent_outcome"]["output"] is not None:
            if question_num <= len(qas):
                return "rate_answer"
            else:
                return "markdown"
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
    
    async def rate_answer(self,state: AgentState):
        chat_history= state['chat_history']
        response = await self.get_agent_executer().ainvoke({"input":self.get_qa_prompt(state),"chat_history":chat_history})
        return {"agent_outcome": response,"question_number":state['question_number']+1}
    
    async def generate_markdown(self,state: AgentState):
        response = interview_state.get_evaluation_report()
        return {"agent_outcome": {"output":response}}
   
    
    def get_qa_prompt(self,state:AgentState):
        programming_language:str=interview_state.get_by_key("programming_language")
        question_num = state["question_number"]
        qa = interview_state.get_question_answer(state["question_number"])
        prompt=f"""
            Rate the answer provided by the user in {programming_language} interview.

            Question Number:
            {question_num}

            Question: 
            {qa.question}

            User Answer:
            {qa.answer}
            
            Follow the below instructions:
            ## Step 1
            - Generate the correct answer for the question.
            - Generate rating for the user answer comparing it with the correct answer.
            - Generate explanation for the rating.
            ## Step 2
            Save the generated correct answer,rating, explanation and question number using tools.
            """
        return prompt
    

    

