import operator

from typing import Annotated, List, Any, Dict
from dataclasses import dataclass, field

from langchain_tavily import TavilySearch

from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, BaseMessage, AnyMessage

from typing_extensions import TypedDict

import sqlite3

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)