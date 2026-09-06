from pydantic import BaseModel
from typing import Annotated
from dotenv import load_dotenv

from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq


load_dotenv()


# State
class State(BaseModel):
    messages: Annotated[list, add_messages]


# Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    
)



# Node
def chatbot(state: State):

    response = llm.invoke(state.messages)

    return {
        "messages": [
            {
                "role": "assistant",
                "content": response.content
            }
        ]
    }


# Graph
graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

app = graph.compile()


# Run
question = input("ASK: ")

result = app.invoke({
    "messages": [
        {
            "role": "user",
            "content": question
        }
    ]
})

print(result["messages"][-1].content)