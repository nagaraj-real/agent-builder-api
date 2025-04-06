from pathlib import Path
from typing import Any, Literal
from langchain_core.messages import AIMessage,ToolMessage
from agentbuilder.agents.params import AgentBuilderParams
from agentbuilder.agents.prompt_helper import get_default_agent_prompt
from agentbuilder.data import data_path
from langchain_core.agents import AgentAction
from typing import TypedDict, Annotated
from langchain_core.runnables.graph import MermaidDrawMethod
from agentbuilder.llm import chat_llm as default_llm
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

def add_messages(left: list, right: list):
    """Add-don't-overwrite."""
    return left + right

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


class BaseGraphAgentBuilder:

    def __init__(self,params:AgentBuilderParams):
        self.intermediate_steps=[]
        self.builder_params=params
        self.initialize_state()
        self.initialize_graph()
        self.save_graph(params.name)

    def initialize_state(self):
        self.builder= StateGraph(AgentState)

    def initialize_graph(self):
        tool_node = ToolNode(self.builder_params.tools)
        self.builder.add_node("agent", self.call_model)
        self.builder.add_node("tools", tool_node)
        self.builder.set_entry_point("agent")
        self.builder.add_conditional_edges(
            "agent",
            self.should_continue,
        )
        self.builder.add_edge('tools', "agent")
    
    def should_continue(self,state: AgentState) -> Literal["tools", "__end__"]:
        messages = state['messages']
        for message in messages:
            if isinstance(message,ToolMessage):
                t = next(item for item in self.intermediate_steps if item['tool_call_id'] == message.tool_call_id)
                t['tool_output'] = message.content
        last_message = messages[-1]
        if last_message.tool_calls:
            for tool in last_message.tool_calls:
                self.intermediate_steps.append({"tool_call_id":tool['id'],"tool":tool["name"],"tool_input":tool["args"],"tool_output":""})
            return "tools"
        return "__end__"

    def call_model(self,state: AgentState):
        messages = state['messages']
        llm= self.builder_params.chat_llm or default_llm
        model = llm.bind_tools(self.builder_params.tools)
        response = model.invoke(messages)
        return {"messages": [response]}

        
    def get_intermediate_steps(self):
        return [(AgentAction(tool=step["tool"],
                             tool_input=step["tool_input"],log=""),
                             step["tool_output"]) for step in self.intermediate_steps]

    def compile(self):
        return self.builder.compile()
    
    def save_graph(self,file_name):
        from IPython.display import Image
        img:Any= Image(
                self.compile().get_graph().draw_mermaid_png(
                    draw_method=MermaidDrawMethod.API,
                )
            )
        with open(f"{data_path}/{file_name}.png", "wb") as fout:
            fout.write(img.data)
        
    
    def input_parser(self,params):
        preamble = self.builder_params.preamble
        input = params["input"]
        chat_history= params["chat_history"]
        prompt = get_default_agent_prompt(preamble)
        messages = prompt.format_messages(input=input,chat_history=chat_history)
        return {"messages":messages}
    
    def message_output_parser(self,messages_dict:dict):
         if "messages" in messages_dict:
            messages = messages_dict['messages']
            if messages and isinstance(messages[-1],AIMessage):
                return {"output":messages[-1].content}

    async def ainvoke(self,params):
        runnable=  self.compile()
        response = await runnable.ainvoke(self.input_parser(params))
        messages_dict = response
        parsed_response = self.message_output_parser(messages_dict)
        parsed_response["intermediate_steps"] = self.get_intermediate_steps()
        return parsed_response
    
    def astream(self,params):
        runnable=  self.compile()
        response= runnable.astream(self.input_parser(params),stream_mode="updates")
        async def gen():
            async for output in response:
                for _, value in output.items():
                    output_dict= self.message_output_parser(value)
                    if(output_dict):
                        yield output_dict
            yield {"intermediate_steps": self.get_intermediate_steps()}
        return gen()

    

