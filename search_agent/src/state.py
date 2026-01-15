import operator
import sqlite3

from typing import Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

context = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(context)