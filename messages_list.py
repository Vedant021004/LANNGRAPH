from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END


class State(BaseModel):
    Messages: list



def fun1(state: State):
    print("Before:", state.Messages)

    state.Messages.append("Message added by fun1")

    print("After:", state.Messages)


def fun2(state: State):
    print("I am second")


def rivk(state: State):
    print("Messages:", state.Messages)


graph = StateGraph(State)

graph.add_node("node_1", fun1)
graph.add_node("node_2", fun2)
graph.add_node("node_3", rivk)

graph.add_edge(START, "node_1")
graph.add_edge("node_1", "node_2")
graph.add_edge("node_2", "node_3")
graph.add_edge("node_3", END)

mwaah = graph.compile()


result = mwaah.invoke({
    "Messages": [
        1,
        "How are you?",
        "I am learning LangGraph"
    ]
})