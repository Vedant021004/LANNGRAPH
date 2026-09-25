from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
)


class State(TypedDict):
    topic: str
    answer: str
    decision: str
    final_answer: str


def explain_topic(state: State):

    response = llm.invoke(
        f"Explain {state['topic']} clearly for a beginner."
    )

    print("\nInitial Explanation:\n")
    print(response.content)

    return {
        "answer": response.content
    }


def ask_human(state: State):

    decision = interrupt(
        f"""
Topic: {state['topic']}

Should I process further on this topic?
Type yes or no.
"""
    )

    return {
        "decision": decision.lower()
    }


def route(state: State):

    if state["decision"] == "yes":
        return "continue"

    return "stop"


def process_further(state: State):

    response = llm.invoke(
        f"""
We were discussing: {state['topic']}

Here is the previous explanation:

{state['answer']}

Now process this topic further.
Explain deeper concepts, examples, and practical applications.
"""

    )

    return {
        "final_answer": response.content
    }


def stop(state: State):

    return {
        "final_answer": state["answer"]
    }


builder = StateGraph(State)

builder.add_node("explain", explain_topic)
builder.add_node("human_review", ask_human)
builder.add_node("continue", process_further)
builder.add_node("stop", stop)

builder.add_edge(START, "explain")
builder.add_edge("explain", "human_review")

builder.add_conditional_edges(
    "human_review",
    route,
    {
        "continue": "continue",
        "stop": "stop"
    }
)

builder.add_edge("continue", END)
builder.add_edge("stop", END)

graph = builder.compile(
    checkpointer=InMemorySaver()
)


config = {
    "configurable": {
        "thread_id": "topic-1"
    }
}


topic = input("Enter topic: ")

graph.invoke(
    {
        "topic": topic
    },
    config
)

decision = input("\nShould I process further? yes/no: ")

result = graph.invoke(
    Command(resume=decision),
    config
)

print("\nFinal Result:\n")
print(result["final_answer"])