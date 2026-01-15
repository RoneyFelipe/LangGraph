from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from src.tools import TOOLS
from src.state import memory
from src.graph import Agent
from src.prompts import prompt_system
import uuid

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash") # Recomendo usar nomes estáveis, o '3-preview' pode ser instável

abot = Agent(model, TOOLS, system=prompt_system, checkpointer=memory)

thread_id = "sessao_teste_1"
thread = {"configurable": {"thread_id": thread_id}}

print("--- Assistente Iniciado (Digite 'q' para sair) ---")

while True:
    user_input = input("\nVocê: ")
    if user_input.lower() in ['q', 'quit', 'sair']:
        break

    messages = [HumanMessage(content=user_input)]
    
    for event in abot.graph.stream({"messages": messages}, thread, stream_mode="values"):
        message = event["messages"][-1]
        
        if hasattr(message, "content") and message.content:

            sender = "IA" if message.type == "ai" else "Tool" if message.type == "tool" else "Humano"
            
            if sender != "Humano":
                print(f"[{sender}]: {message.content}")