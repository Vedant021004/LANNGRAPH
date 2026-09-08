from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)


# State
class State(BaseModel):
    question: str
    route: str = ""
    answer: str = ""


# 1. CLASSIFIER
def classifier(state: State):

    result = llm.invoke(
        f"""
        Classify this question as only one of:
        coding
        general

        Question: {state.question}

        Reply only coding or general.
        """
    )

    return {"route": result.content.strip().lower()}


# 2. ROUTER DECISION
def routing(state: State):

    return state.route


# 3. CODING NODE
def coding(state: State):

    result = llm.invoke(
        f"Answer this as a coding expert: {state.question}"
    )

    return {"answer": result.content}


# 4. GENERAL NODE
def general(state: State):

    result = llm.invoke(
        f"Answer this as a general expert: {state.question}"
    )

    return {"answer": result.content}


# Create graph
graph = StateGraph(State)


# Add nodes
graph.add_node("classifier", classifier)
graph.add_node("coding", coding)
graph.add_node("general", general)


# START → classifier
graph.add_edge(START, "classifier")


# CLASSIFIER → routing → correct node
graph.add_conditional_edges(
    "classifier",
    routing,
    {
        "coding": "coding",
        "general": "general"
    }
)


# Nodes → END
graph.add_edge("coding", END)
graph.add_edge("general", END)


# Compile
app = graph.compile()


# User input
q = input("Ask: ")


# Start graph
result = app.invoke(
    State(question=q)
)


# Final answer
print(result["answer"])