from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()

conn = sqlite3.connect(
    "checkpoints.db",
    check_same_thread=False
)

checkpointer = SqliteSaver(conn)

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)


class State(BaseModel):
    question: str
    answer: str = ""
    decision: str = ""
    final_answer: str = ""


def generate_answer(state: State):
    response = llm.invoke(
        f"""
You are a helpful AI assistant.

Answer this question clearly for a beginner:

{state.question}
"""
    )

    print("\nAI Answer:\n")
    print(response.content)

    return {
        "answer": response.content
    }


def ask_user(state: State):
    decision = interrupt(
        "Do you want further details? Type yes or no."
    )

    return {
        "decision": decision.lower()
    }


def route(state: State):

    if state.decision == "yes":
        return "further"

    return "finish"


def further_details(state: State):

    response = llm.invoke(
        f"""
We were discussing this topic:

{state.question}

Here was the first answer:

{state.answer}

Now provide further details.

Explain:
- deeper concepts
- examples
- practical applications
- important points

Do not repeat the entire previous answer.
"""
    )

    return {
        "final_answer": response.content
    }


def finish(state: State):

    return {
        "final_answer": state.answer
    }


builder = StateGraph(State)

builder.add_node("generate", generate_answer)
builder.add_node("ask_user", ask_user)
builder.add_node("further", further_details)
builder.add_node("finish", finish)

builder.add_edge(START, "generate")
builder.add_edge("generate", "ask_user")

builder.add_conditional_edges(
    "ask_user",
    route,
    {
        "further": "further",
        "finish": "finish"
    }
)

builder.add_edge("further", END)
builder.add_edge("finish", END)

graph = builder.compile(
    checkpointer=checkpointer
)


config = {
    "configurable": {
        "thread_id": "topic-1"
    }
}


question = input("Enter your question: ")

graph.invoke(
    {
        "question": question
    },
    config
)

user_input = input(
    "\nDo you want further details? yes/no: "
)

result = graph.invoke(
    Command(resume=user_input),
    config
)

print("\nFinal Result:\n")
print(result["final_answer"]) 