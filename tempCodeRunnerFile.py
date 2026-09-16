from langchain_core.tools import tool


@tool
def addition(a: int, b: int):
    """Add two numbers."""
    return a + b


print(addition)
print(addition.name)
print(addition.description)
print(addition.args_schema)