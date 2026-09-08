from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

class State(BaseModel):
    question: str
    route: str = ""
    answer: str = ""

def classifier(state: State):

    result = llm.invoke(
        f"""
        Classify the customer question into ONLY one category:

        billing
        technical
        orders

        Question: {state.question}

        Reply only with the category.
        """
    )

    return {
        "route": result.content.strip().lower()
    }

def router(state: State):

    return state.route

def billing(state: State):

    result = llm.invoke(
        f"""
        You are a billing support expert.

        Answer the customer question:
        {state.question}
        """
    )

    return {
        "answer": result.content
    }

def technical(state: State):

    result = llm.invoke(
        f"""
        You are a technical support expert.

        Answer the customer question:
        {state.question}
        """
    )

    return {
        "answer": result.content
    }

def orders(state: State):

    result = llm.invoke(
        f"""
        You are an order support expert.

        Answer the customer question:
        {state.question}
        """
    )

    return {
        "answer": result.content
    }

graph = StateGraph(State)


graph.add_node("classifier", classifier)
graph.add_node("billing", billing)
graph.add_node("technical", technical)
graph.add_node("orders", orders)


graph.add_edge(START, "classifier")


graph.add_conditional_edges(
    "classifier",
    router,
    {
        "billing": "billing",
        "technical": "technical",
        "orders": "orders"
    }
)


graph.add_edge("billing", END)
graph.add_edge("technical", END)
graph.add_edge("orders", END)


app = graph.compile()

q = input("Customer: ")

result = app.invoke(
    State(question=q)
)

print("\nRoute:", result["route"])
print("\nAnswer:", result["answer"])