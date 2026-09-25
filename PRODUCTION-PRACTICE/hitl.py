from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver


class State(TypedDict):
    answer: str
    result: str


def ask_user(state: State):

    answer = interrupt("Do you want to continue? yes/no")

    return {
        "answer": answer
    }


def process(state: State):

    if state["answer"].lower() == "yes":
        print("YES - Workflow resumed")
        return {
            "result": "User approved"
        }

    print("NO - Workflow stopped")

    return {
        "result": "User rejected"
    }


def final_node(state: State):

    print("Final Node Executed")
    print("Result:", state["result"])

    return {}


builder = StateGraph(State)

builder.add_node("ask_user", ask_user)
builder.add_node("process", process)
builder.add_node("final", final_node)

builder.add_edge(START, "ask_user")
builder.add_edge("ask_user", "process")
builder.add_edge("process", "final")
builder.add_edge("final", END)

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

result = graph.invoke(
    Command(resume=user_input),
    config
)

print(result)