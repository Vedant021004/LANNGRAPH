from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END


# -----------------------------
# STATE
# -----------------------------

class State(BaseModel):
    weight: float
    height: float
    bmi: float = 0.0


# -----------------------------
# BMI NODE
# -----------------------------

def calculate_bmi(state: State):

    state.bmi = state.weight / (state.height ** 2)

    return state


def judge(state:State):

    if state.bmi > 0:
        print("over weight")
    else:
        print("under weight")    
# -----------------------------
# GRAPH
# -----------------------------

graph = StateGraph(State)

graph.add_node("BMI", calculate_bmi)
graph.add_node("check",judge)

graph.add_edge(START, "BMI")
graph.add_edge("BMI", "check")
graph.add_edge("check",END)

app = graph.compile()


# -----------------------------
# USER INPUT
# -----------------------------

weight = float(input("Weight (kg): "))
height = float(input("Height (m): "))


# -----------------------------
# RUN GRAPH
# -----------------------------

result = app.invoke({
    "weight": weight,
    "height": height,
    "bmi": 0.0
})


print("BMI:", round(result["bmi"], 2))