from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from pydantic import BaseModel
from typing import Annotated


@tool
def add(a: int, b: int):
    """Add two numbers."""
    return a + b


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

llm = llm.bind_tools([add])


class State(BaseModel):
    messages: Annotated[list, add_messages]


def chatbot(state):
    return {
        "messages": [llm.invoke(state.messages)]
    }


graph = StateGraph(State)

graph.add_node("chatbot", chatbot)
graph.add_node("tools", ToolNode([add]))

graph.add_edge(START, "chatbot")

graph.add_conditional_edges(
    "chatbot",
    tools_condition
)

graph.add_edge("tools", "chatbot")

graph.add_edge("chatbot", END)

app = graph.compile()


result = app.invoke({
    "messages": [
        ("user", "What is 7 + 9?")
    ]
})

print(result["messages"][-1].content)