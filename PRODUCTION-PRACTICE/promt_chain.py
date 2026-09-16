from pydantic import BaseModel
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

load_dotenv()

class State(BaseModel):
    question: str = ""
    outline: str = ""
    answer: str = ""

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

def first_llm(state: State):
    outline = llm.invoke(
        f"""
        Generate a detailed outline for the following topic:

        Topic:
        {state.question}

        Include:
        - Introduction
        - Main sections
        - Important points
        - Conclusion
        """
    ).content

    return {
        "outline": outline
    }

def second_llm(state: State):
    blog = llm.invoke(
        f"""
        Write a complete blog about the following topic.

        Topic:
        {state.question}

        Use this outline:

        {state.outline}

        Follow the outline carefully and write a clear,
        detailed and readable blog.
        """
    ).content

    return {
        "answer": blog
    }

graph = StateGraph(State)

graph.add_node("FIRST", first_llm)
graph.add_node("SECOND", second_llm)

graph.add_edge(START, "FIRST")
graph.add_edge("FIRST", "SECOND")
graph.add_edge("SECOND", END)

app = graph.compile()

ask = input("ASK: ")

result = app.invoke(
    State(question=ask)
)

print(result["answer"])