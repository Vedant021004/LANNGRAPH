from pydantic import BaseModel # best opt
from langgraph.graph import StateGraph, START, END # poora graph ka structure hai 


class State(BaseModel):
    message: str


def node_a(state: State):
    return {"message": state.message + " → Node A"}


def node_b(state: State):
    return {"message": state.message + " → Node B"}


graph = StateGraph(State)

graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)

graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", END)

app = graph.compile()

result = app.invoke(State(message="Start"))

print(result)