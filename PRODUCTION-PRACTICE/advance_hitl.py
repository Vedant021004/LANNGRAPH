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
    request: str
    draft: str
    risk: str
    decision: str
    feedback: str
    final_answer: str


def generate_draft(state: State):

    response = llm.invoke(
        f"""
Create a response for this user request:

{state['request']}
"""
    )

    return {
        "draft": response.content
    }


def analyze_risk(state: State):

    response = llm.invoke(
        f"""
Analyze this request:

{state['request']}

Classify the risk as only:
LOW
or
HIGH

Return only LOW or HIGH.
"""
    )

    risk = response.content.strip().upper()

    if "HIGH" in risk:
        risk = "HIGH"
    else:
        risk = "LOW"

    return {
        "risk": risk
    }


def route_risk(state: State):

    if state["risk"] == "HIGH":
        return "human_review"

    return "automatic"


def human_review(state: State):

    review = interrupt(
        {
            "message": "Human review required",
            "request": state["request"],
            "draft": state["draft"],
            "options": [
                "approve",
                "reject",
                "edit"
            ]
        }
    )

    return {
        "decision": review["decision"],
        "feedback": review.get("feedback", "")
    }


def route_decision(state: State):

    if state["decision"] == "approve":
        return "final"

    if state["decision"] == "edit":
        return "edit"

    return "reject"


def edit_response(state: State):

    response = llm.invoke(
        f"""
Original request:

{state['request']}

Original draft:

{state['draft']}

Human feedback:

{state['feedback']}

Create an improved final response using the human feedback.
"""
    )

    return {
        "final_answer": response.content
    }


def automatic_response(state: State):

    return {
        "final_answer": state["draft"]
    }


def final_response(state: State):

    return {
        "final_answer": state["draft"]
    }


def reject_response(state: State):

    return {
        "final_answer": "The request was rejected by human review."
    }


builder = StateGraph(State)

builder.add_node("generate", generate_draft)
builder.add_node("risk", analyze_risk)
builder.add_node("human_review", human_review)
builder.add_node("automatic", automatic_response)
builder.add_node("final", final_response)
builder.add_node("edit", edit_response)
builder.add_node("reject", reject_response)

builder.add_edge(START, "generate")
builder.add_edge("generate", "risk")

builder.add_conditional_edges(
    "risk",
    route_risk,
    {
        "human_review": "human_review",
        "automatic": "automatic"
    }
)

builder.add_conditional_edges(
    "human_review",
    route_decision,
    {
        "final": "final",
        "edit": "edit",
        "reject": "reject"
    }
)

builder.add_edge("automatic", END)
builder.add_edge("final", END)
builder.add_edge("edit", END)
builder.add_edge("reject", END)

graph = builder.compile(
    checkpointer=InMemorySaver()
)


config = {
    "configurable": {
        "thread_id": "advanced-hitl-1"
    }
}


request = input("Enter request: ")

result = graph.invoke(
    {
        "request": request
    },
    config
)

if "__interrupt__" in result:

    print("\nHUMAN REVIEW REQUIRED")
    print(result["__interrupt__"])

    decision = input(
        "\nDecision (approve/reject/edit): "
    )

    feedback = ""

    if decision == "edit":
        feedback = input("Enter feedback: ")

    result = graph.invoke(
        Command(
            resume={
                "decision": decision,
                "feedback": feedback
            }
        ),
        config
    )


print("\nFINAL ANSWER:")
print(result["final_answer"])