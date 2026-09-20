from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import Annotated
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

model = ChatGroq(
    model="openai/gpt-oss-20b"
)

class State(BaseModel):

    Messages: Annotated[
        list,
        add_messages
    ] = Field(default_factory=list)

def node(state: State):

    result = model.invoke(
        state.Messages
    )

    return {
        "Messages": [result]
    }

checkpointer = MemorySaver()

graph = StateGraph(State)

graph.add_node(
    "first",
    node
)

graph.add_edge(
    START,
    "first"
)

graph.add_edge(
    "first",
    END
)


# Compile graph with memory
app = graph.compile(
    checkpointer=checkpointer
)

while True:

    user = input("ASK: ")

    # Exit condition
    if user.lower() in ["exit", "quit", "bye"]:
        print("Chat ended.")
        break

    human_message = HumanMessage(
        content=user
    )

    ans = app.invoke(
        {
            "Messages": [human_message]
        },
        config={
            "configurable": {
                "thread_id": '1'
            }
        }
    )

    print(
        "AI:",
        ans["Messages"][-1].content
    )