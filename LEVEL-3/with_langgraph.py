from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode


def add(a: int, b: int):
    return a + b


llm = ChatGroq(
    model="openai/gpt-oss-20b"
)

llm = llm.bind_tools([add])

tool_node = ToolNode([add])


user = input("ASK: ")
result = llm.invoke(user)

print(result.tool_calls)

tool_result = tool_node.invoke({
    "messages": [result]
})

print(tool_result)