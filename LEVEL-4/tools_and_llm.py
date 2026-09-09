from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from typing import Annotated



def add(a:int, b:int):
    """ADD TWO NUMBERS"""
    return a+b


def add(a:int, b:int):
    """ADD TWO NUMBERS"""
    return a+b