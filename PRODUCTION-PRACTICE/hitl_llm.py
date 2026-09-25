from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)


class State(TypedDict):
    question: str
    answer: str
    approved: bool
    result: str


def generate(state:State):

    response = llm.invoke(
        f""" answer this question : \n {state["question"]}"""
    )

    return {
        "answer" : response.content
    }


def intereupt(state:State):

    decision = interrupt(
        f""" ai generated this answer 
        {state["answer"]}
        do you approved this answer ?
         type yes or no  """
    )

    return {
        "approved": decision.lower() == "yes"
    }


