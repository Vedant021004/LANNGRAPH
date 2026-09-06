from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END


class State(BaseModel):
    number: int


def check_number(state: State):
    print("Checking number...")
    return state


def decide(state: State):

    if state.number > 10:
        return "big"
    else:
        return "small"


def big(state: State):
    print("Number is BIG")
    return state


def small(state: State):
    print("Number is SMALL")
    return state


graph = StateGraph(State)

graph.add_node("check", check_number)
graph.add_node("big", big)
graph.add_node("small", small)

graph.add_edge(START, "check")

graph.add_conditional_edges(
    "check",
    decide,
    {
        "big": "big",
        "small": "small"
    }
)

graph.add_edge("big", END)
graph.add_edge("small", END)


app = graph.compile()

user = int(input("Ask: "))
result = app.invoke({
    "number": user
})