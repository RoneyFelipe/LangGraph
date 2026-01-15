from langchain_core.tools import BaseTool, tool
from langchain_tavily import TavilySearch
from src.state import context
import sqlite3

from src.configs import TAVILY_API_KEY

@tool
def calculator(expression: str) -> str:
    """Calcula o resultado de uma expressão matemática.
    
    Args:
        expression (str): A conta matemática a ser feita (ex: "2 + 2", "5 * 10").
        
    Returns:
        str: O resultado numérico da conta.
    """
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Erro: {e}"

@tool
def reset_memory() -> str:
    """
    Apaga, limpa ou deleta todo o histórico e contexto da conversa armazenado no banco de dados.
    Use esta ferramenta IMEDIATAMENTE se o usuário pedir 'DELETE O CONTEXTO', 'Limpar memória' ou 'Esquecer tudo'.
    """
    connection = None
    try:
        connection = sqlite3.connect("checkpoints.db")
        cursor = connection.cursor()
    
        cursor.execute("DELETE FROM checkpoints")
        cursor.execute("DELETE FROM writes")
        connection.commit()
        
        return "Contexto deletado com sucesso. A memória estará vazia na próxima mensagem."
    except Exception as e:
        return f"Erro ao deletar contexto: {e}"
    finally:
        if connection:
            connection.close()


tavily_search = TavilySearch(max_results=3, tavily_api_key=TAVILY_API_KEY)

    
TOOLS: list[BaseTool] = [tavily_search, calculator, reset_memory]