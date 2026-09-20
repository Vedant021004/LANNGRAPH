from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
from typing import TypedDict, Literal
import operator

load_dotenv()


# =========================
# LLM
# =========================

model = ChatGroq(
    model="openai/gpt-oss-20b",
    
)


class SentimentSchema(BaseModel):

    sentiment: Literal["positive", "negative"] = Field(description='Sentiment of the review')


structured_model = model.with_structured_output(
    SentimentSchema,
    method="json_schema"
)

class State(TypedDict):

    review: str
    sentiment: Literal["positive", "negative"]
    diagnosis: dict
    response: str



def find_sentiment(state:State):
    promt = f"for the following review find out eht sentiment {state["review"]}"

    sentiment = structured_model.invoke(promt).sentiment

    return{
        "sentiment" : sentiment
    }


def check_sentiment(state: State) -> Literal["positive_response", "run_diagnosis"]:

    if state['sentiment'] == 'positive':
        return 'positive_response'
    else:
        return 'run_diagnosis'

def positive_response(state:State):

    prompt = f"""Write a warm thank-you message in response to this review:
    \n\n\"{state['review']}\"\n
Also, kindly ask the user to leave feedback on our website."""
    
    response = model.invoke(prompt).content

    return {'response': response}    


    


graph = StateGraph(State)

graph.add_node("FIRST", find_sentiment)

graph.add_edge(START , "FIRST")
graph.add_edge("FIRST" , END)

add = graph.compile()







  