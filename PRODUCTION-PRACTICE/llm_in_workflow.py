from pydantic import BaseModel
from typing import Annotated
from dotenv import load_dotenv

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq


load_dotenv()


# State
class State(BaseModel):
    question : str = ""

    answer : str = ""


# Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    
)

def cahtbot(state:State):
    model = llm.invoke(state.question)

    return {

        "answer" : model.content
    }

graph = StateGraph(State)
graph.add_node("LLM", cahtbot)
graph.add_edge(START,"LLM")
graph.add_edge("LLM",END)

result = graph.compile()

q = input("ASK: ")

app = result.invoke(
        State(question=q)
)

print(app["answer"])


