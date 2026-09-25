# from langgraph.graph import StateGraph, START, END
# from langchain_groq import ChatGroq
# from dotenv import load_dotenv
# from typing import TypedDict, Annotated
# from pydantic import BaseModel, Field
# from typing import TypedDict, Literal
# from langchain_core.prompts import ChatPromptTemplate
# import operator

# load_dotenv()



# load_dotenv()


# generator = ChatGroq(
#     model="openai/gpt-oss-20b",
#     temperature=0
# )

# optimizer = ChatGroq(
#     model="openai/gpt-oss-20b",
#     temperature=0
# )

# evaluator = ChatGroq(
#     model="openai/gpt-oss-120b",
#     temperature=0
# )


# class TweetState(TypedDict):

#     topic: str
#     tweet: str
#     evaluation: Literal["approved", "needs_improvement"]
#     feedback: str
#     iteration: int
#     max_iteration: int 


# def generateor(state:TweetState):
    
#     prompt = ChatPromptTemplate.from_messages([


#         ("SystemMessage","You are a funny and clever Twitter/X influencer."),
#         ("HumanMessage",f"""
#         Write a short, original, and hilarious tweet on the topic: "{state['topic']}".

#         Rules:
#         - Do NOT use question-answer format.
#         - Max 280 characters.
#         - Use observational humor, irony, sarcasm, or cultural references.
#         - Think in meme logic, punchlines, or relatable takes.
#         - Use simple, day to day english
#         """)
#     ]

#     messages = prompt.invoke({
#     "question": "What is RAG?"
#     })

    






