from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver


class State(TypedDict):
    answer: str


def ask_user(state: State):

    answer = interrupt("Do you want to continue?")

    return {
        "answer": answer
    }


def after_resume(state: State):

    print("Workflow resumed!")
    print("Human said:", state["answer"])

    return {}


builder = StateGraph(State)

builder.add_node("ask_user", ask_user)
builder.add_node("after_resume", after_resume)

builder.add_edge(START, "ask_user")
builder.add_edge("ask_user", "after_resume")
builder.add_edge("after_resume", END)

graph = builder.compile(
    checkpointer=InMemorySaver()
)


config = {
    "configurable": {
        "thread_id": "1"
    }
}


graph.invoke({}, config)

user_input = input("Enter yes/no: ")

graph.invoke(
    Command(resume=user_input),
    config
)