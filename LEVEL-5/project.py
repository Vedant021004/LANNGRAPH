from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel
from langchain_tavily import TavilySearch


load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b"
)


class State(BaseModel):
    question: str
    route: str = ""
    answer: str = ""


def classifier(state: State):
    r = llm.invoke(
        f"""
        Classify this question as only one of:
        tavily,
        addition,
        llm

        Question: {state.question}

        Reply only with one word:
        tavily
        addition
        llm
        """
    )

    return {"route": r.content.strip().lower()}


def decide(state: State):
    return state.route


def addition(a: int, b: int):
    """Add two numbers."""
    return a + b


def tavily(state: State):
    tool = TavilySearch(max_results=2)
    result = tool.invoke(state.question)

    return {"answer": result["results"]}


def general_llm(state: State):
    r = llm.invoke(
        f"""
        You are a helpful AI assistant.

        Answer the user's question clearly, accurately, and concisely.
        Explain the answer in a simple way when necessary.

        User question:
        {state.question}
        """
    )

    return {"answer": r.content}


# -----------------------------
# Build LangGraph
# -----------------------------

graph = StateGraph(State)

# Add nodes
graph.add_node("classifier", classifier)
graph.add_node("tavily", tavily)
graph.add_node("addition", addition)
graph.add_node("general_llm", general_llm)

# START → classifier
graph.add_edge(START, "classifier")

# classifier → decide → appropriate node
graph.add_conditional_edges(
    "classifier",
    decide,
    {
        "tavily": "tavily",
        "addition": "addition",
        "llm": "general_llm"
    }
)

# Each route → END
graph.add_edge("tavily", END)
graph.add_edge("addition", END)
graph.add_edge("general_llm", END)

# Compile graph
app = graph.compile()


# -----------------------------
# Run
# -----------------------------

question = input("Ask: ")

result = app.invoke(
    State(question=question)
)

print("\nRoute:", result["route"])
print("Answer:", result["answer"])