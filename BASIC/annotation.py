from typing import Annotated
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_ollama import ChatOllama


llm = ChatOllama(model="qwen3:latest")


class State(BaseModel):
    messages: Annotated[list, add_messages]


# node

def chatbot(state: State):

    # Send messages to AI
    response = llm.invoke(state.messages)

    # Store AI response
    return {
        "messages": [response]
    }


graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()


user_input = input("You: ")

result = app.invoke({
    "messages": [user_input]
})


print("AI:", result["messages"][-1].content)