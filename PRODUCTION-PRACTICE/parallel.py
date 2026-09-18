from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()


# ---------------- STATE ----------------

class State(BaseModel):
    name: str
    age: str
    location: str

    greeting: str = ""
    age_info: str = ""
    location_info: str = ""
    summary: str = ""


# ---------------- NODE 1 ----------------

def greet(state: State):

    greeting = f"Hello {state.name}! Welcome to the system."

    return {
        "greeting": greeting
    }


# ---------------- NODE 2 ----------------

def age_info(state: State):

    age_info = f"You are {state.age} years old."

    return {
        "age_info": age_info
    }


# ---------------- NODE 3 ----------------

def location(state: State):

    location_info = f"You are currently from {state.location}."

    return {
        "location_info": location_info
    }


# ---------------- SUMMARY ----------------

def summary(state: State):

    final_summary = f"""
{state.greeting}

{state.age_info}

{state.location_info}
"""

    return {
        "summary": final_summary
    }


# ---------------- GRAPH ----------------

graph = StateGraph(State)


graph.add_node("greet", greet)
graph.add_node("age_info", age_info)
graph.add_node("location", location)
graph.add_node("summary", summary)


# START → 3 PARALLEL NODES

graph.add_edge(START, "greet")
graph.add_edge(START, "age_info")
graph.add_edge(START, "location")


# 3 NODES → SUMMARY

graph.add_edge("greet", "summary")
graph.add_edge("age_info", "summary")
graph.add_edge("location", "summary")


# SUMMARY → END

graph.add_edge("summary", END)


app = graph.compile()


# ---------------- USER INPUT ----------------

name = input("Enter your name: ")
age = input("Enter your age: ")
user_location = input("Enter your location: ")


initial_state = State(
    name=name,
    age=age,
    location=user_location
)


# ---------------- RUN ----------------

result = app.invoke(initial_state)


print("\n========== FINAL SUMMARY ==========")
print(result["summary"])