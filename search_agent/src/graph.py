from src.state import AgentState
from stamina import retry
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, ToolMessage

class Agent:

    def __init__(self, model, tools, checkpointer, system=""):
        self.system = system
        
        graph = StateGraph(AgentState)
        
        graph.add_node("llm", self.call_gemini)
        
        graph.add_node("action", self.take_action)
        
        graph.add_conditional_edges("llm", self.exists_action, {True: "action", False: END})
        
        graph.add_edge("action", "llm")
        
        graph.set_entry_point("llm")
        
        self.graph = graph.compile(checkpointer=checkpointer)
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)
    
    @retry(on=Exception, attempts=3, wait_initial=1.0, wait_max=30, wait_jitter=1.0)
    def call_gemini(self, state: AgentState):

        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
            
        print("Mensagens enviadas ao modelo:", messages)
        message = self.model.invoke(messages)
        return {'messages': [message]}
    
    def exists_action(self, state: AgentState):

        result = state['messages'][-1]
        return len(result.tool_calls) > 0
    
    def take_action(self, state: AgentState):

        tool_calls = state['messages'][-1].tool_calls
        results = []

        for tool in tool_calls:

            print(f"Escolhendo a tool: {tool['name']} com os argumentos: {tool['args']}")
            result = self.tools[tool['name']].invoke(tool['args'])
            results.append(ToolMessage(tool_call_id=tool['id'], name=tool['name'], content=str(result)))

        print("Final da ação")
        return {'messages': results}
    
    