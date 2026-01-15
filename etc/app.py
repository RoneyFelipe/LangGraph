import os

from agent import Agent
from agent_state import memory

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import HumanMessage

current_tavily_api_key = os.getenv('TAVILY_KEY')
if not current_tavily_api_key:
    raise ValueError("TAVILY_API_KEY não encontrada. Certifique-se de que está no seu .env e python-dotenv está instalado.")

tool = TavilySearch(max_results=3, tavily_api_key=current_tavily_api_key)

prompt_system = """Você é um assistente de pesquisa inteligente. Use o mecanismo de busca (tavily_search_results_json) para procurar informações.
Você tem permissão para fazer múltiplas chamadas à ferramenta (em conjunto ou em sequência).
Busque informações apenas quando tiver certeza do que procurar.
Se precisar de mais detalhes para formular uma pergunta de acompanhamento, você tem permissão para fazer isso.
Quando solicitado a comparar informações (ex: qual é mais quente, maior, etc.), use as informações do histórico da conversa e dos resultados das ferramentas."""

model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

abot = Agent(model, [tool], system=prompt_system, checkpointer=memory)


messages = [HumanMessage(content="E no Rio de Janeiro?")]
thread = {"configurable": {"thread_id": "1"}}

print("\n--- Pergunta 2: Tempo no Rio de Janeiro ---")
for event in abot.graph.stream({"messages": messages}, thread):
    for k, v in event.items():
        if k in ("llm", "action"):
            print(f"{k}: {v['messages']}")