import sqlite3
from stamina import retry

from langchain_core.tools import BaseTool, tool
from langchain_tavily import TavilySearch
from src.state import context

from src.configs import TAVILY_API_KEY
    
@tool
def calculator(expression):
    """Calcula o resultado de uma expressão matemática.
    
    Args:
        expression (str): A conta matemática a ser feita (ex: "2 + 2", "5 * 10").
        
    Returns:
        st
    """
    try:
        return _calculator_interna(expression)
    except Exception as e:
        return f"Erro sistêmico: Não foi possível calcular '{expression}' após várias tentativas. Detalhe: {e}"

@retry(on=Exception, attempts=3, wait_initial=1.0, wait_max=30, wait_jitter=1.0)
def _calculator_interna(expression):
    return str(eval(expression))

@tool
def reset_memory():
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