import operator
from typing import Annotated, TypedDict
from langchain_core.agents import (
    AgentAction,
)
from agentbuilder.agents.base_graph_agent_builder import AgentState, BaseGraphAgentBuilder
from agentbuilder.agents.interview.data import interview_state
from agentbuilder.agents.params import AgentBuilderParams
from langgraph.graph import StateGraph
from langchain_core.messages import BaseMessage,AIMessage,HumanMessage,SystemMessage
from langgraph.graph import END, StateGraph
from langchain_core.runnables import RunnablePassthrough


class AgentState(TypedDict):
    input: str
    chat_history: list[BaseMessage]
    agent_outcome: AIMessage
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]


class InterviewQuestionAgentBuilder(BaseGraphAgentBuilder):

    def __init__(self,params:AgentBuilderParams):
        super().__init__(params=params)
        self.llm = self.builder_params.chat_llm

    def initialize_graph(self):
        self.builder.add_node("ask_question", self.ask_question)
        self.builder.add_node("save_answer", self.save_answer)
        self.builder.add_node("save_answer_or_question", RunnablePassthrough())

        self.builder.set_entry_point("save_answer_or_question")
        self.builder.add_conditional_edges(
        "save_answer_or_question",
        self.save_answer_or_question,
            {
            "ask_question": "ask_question",
            "save_answer": "save_answer"
            },
        )
        self.builder.add_edge("save_answer","ask_question")
        self.builder.add_edge("ask_question",END)

    def initialize_state(self):
        self.builder= StateGraph(AgentState)


    async def ainvoke(self,params):
        runnable=  self.compile()
        response = await runnable.ainvoke(self.input_parser(params))
        return {'output':response['agent_outcome'].content}

     
    def input_parser(self,params):
        input = params["input"]
        chat_history= params["chat_history"]
        return {"input":input,"chat_history": chat_history,"question_number":1}
    
    async def ask_question(self,state: AgentState):
        qas= interview_state.get_model().question_answers
        max_qas= interview_state.get_model().questions_count
        if(len(qas) >= max_qas):
            return {"agent_outcome": AIMessage(content="")}
        preamble = self.builder_params.preamble
        messages= [SystemMessage(content=preamble),HumanMessage(content=self.get_interview_question_prompt(state))]
        response = await self.llm.ainvoke(messages)
        interview_state.get_model().current_question=response.content
        return {"agent_outcome": response}
    
    
    async def save_answer(self,state: AgentState):
        answer= state['input']
        question = interview_state.get_model().current_question
        interview_state.add_question_answer(question=question,answer=answer)
        interview_state.get_model().current_question=""
        return state
   
    def save_answer_or_question(self,state:AgentState):
         question = interview_state.get_model().current_question
         if not question:
            return "ask_question"
         else:
            return "save_answer"
    
    def get_interview_question_prompt(self,state:AgentState):
        programming_language:str=interview_state.get_by_key("programming_language")
        qas = interview_state.get_question_answers_as_conversation()
        job_summary = interview_state.get_model().job_summary
        total_questions= interview_state.get_model().questions_count
        prompt=f"""
            For {programming_language}, generate a new 'single' programming interview question : <question>
            based on the job summary.

            ## Job Summary
            {job_summary}

            ## Previous Question Answers that the candidate already answered: 
            {qas} 

            ## Total Count of Interview Questions:
            {total_questions}

            Make sure the new question you generate is not repeated and is not part of 'Previous Question Answers'.

            The questions should have the following mix:
            - coding type question that requires the candidate to code - 50%
            - non-coding type question that does not require the candidate to code - 50%
            
            # Important
            - Respond with only 1 question. 
            - **DO NOT** include any other text.
            - **DO NOT** include the question type in output response.

            example output: 'Write a code to generate fibonnaci sequence'
            """
        return prompt


    

