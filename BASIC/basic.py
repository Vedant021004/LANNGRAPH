from pydantic import BaseModel # best opt
from langgraph.graph import StateGraph, START, END # poora graph ka structure hai 

class State(BaseModel):
    Messages : str

def fun1(state: State):
    print("first message is :", state.Messages)

def fun2(state: State):
    print("i m second")

def rivk(state :State):
    print("vedant is the husband of :", state.Messages)

graph = StateGraph(State)    

graph.add_node("node_1", fun1)
graph.add_node("node_2", fun2)
graph.add_node("node_3", rivk)

graph.add_edge(START,"node_1")
graph.add_edge("node_1","node_2")
graph.add_edge("node_2", "node_3")
graph.add_edge("node_3",END)


mwaah = graph.compile()

result = mwaah.invoke({ "Messages" : "riddhi kapil "})





