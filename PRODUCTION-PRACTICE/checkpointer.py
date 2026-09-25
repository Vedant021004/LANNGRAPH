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

checkpointer = MemorySaver()

class State(BaseModel):
    question : str
    messages : Annotated[list,add_messages] = Field(default_factory=list)


def joke(state:State):
    question = state.question

    res = model.invoke(
        f""" you are a comedian so crack the jk on this topic{question}"""
    )

    return {
        "messages" : [res]
    }


def explain(state: State):

    joke = state.messages[-1].content

    res = model.invoke(
        f"""
        You are an expert teacher.

        Explain the following joke in simple language.
        Tell me:
        1. What does the joke mean?
        2. Why is it funny?
        3. Is there any wordplay?

        Joke:
        {joke}
        """
    )

    return {
        "messages": [res]
    }

graph = StateGraph(State)

graph.add_node("joke", joke)
graph.add_node("explain", explain)
graph.add_edge(START,"joke")
graph.add_edge("joke","explain")
graph.add_edge("explain",END)

result = graph.compile(checkpointer=checkpointer)

while True:

    user = input("ASK: ")

    answer = result.invoke(

            State(question = user),
            config={
                "configurable": {
                    "thread_id": '1'
                }
            }

    )

    print(answer["messages"][-1].content)