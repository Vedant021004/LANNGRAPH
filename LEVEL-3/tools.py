from langchain_groq import ChatGroq
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()



def add(a: int, b: int):
    """Add two numbers."""
    return a + b


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0
)

llm_with_tools = llm.bind_tools([add])


user = input("ASK: ")
result = llm_with_tools.invoke(user)

tool_result = add.invoke(result.tool_calls[0]["args"])

print(tool_result)