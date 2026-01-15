import operator

from typing import Annotated, List, Any, Dict
from dataclasses import dataclass, field

from langchain_tavily import TavilySearch

from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, BaseMessage, AnyMessage

from typing_extensions import TypedDict

import sqlite3

import os
from dotenv import load_dotenv

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GEMINI_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_KEY')

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

conn = sqlite3.connect("checkpoints.db", check_same_thread=False)
memory = SqliteSaver(conn)