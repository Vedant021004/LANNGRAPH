# LangChain Tools & LangGraph ToolNode — Simple Guide

A simple reference for understanding `@tool`, `bind_tools()`, `**args`, and `ToolNode`.

---

## 🧠 The Big Picture

There are **three different concepts**:

```text
@tool
  ↓
Makes a Python function a LangChain Tool

bind_tools()
  ↓
Gives the LLM access to the Tool

ToolNode
  ↓
Executes the Tool inside LangGraph
```

---

## 1. `@tool` — Create a LangChain Tool

Use `@tool` when you want to turn your Python function into a proper LangChain Tool.

```python
from langchain_core.tools import tool

@tool
def add(a: int, b: int):
    """Add two numbers."""
    return a + b
```

Now `add` is a LangChain Tool.

You can execute it with:

```python
add.invoke({
    "a": 2,
    "b": 3
})
```

Output:

```text
5
```

---

## 2. `bind_tools()` — Give Tools to the LLM

```python
llm_with_tools = llm.bind_tools([add])
```

This tells the LLM:

> "You have access to the `add` tool."

For example:

```python
result = llm_with_tools.invoke(
    "What is 10 + 20?"
)
```

The LLM can return a tool call:

```python
{
    "name": "add",
    "args": {
        "a": 10,
        "b": 20
    }
}
```

⚠️ **Important:** `bind_tools()` does **not** execute the tool.

It only allows the LLM to request the tool.

---

## 3. `**args` — Normal Python

You don't need LangChain for this.

Suppose:

```python
def add(a, b):
    return a + b
```

And:

```python
args = {
    "a": 10,
    "b": 20
}
```

You can execute:

```python
add(**args)
```

Python converts this:

```python
add(**{"a": 10, "b": 20})
```

into:

```python
add(a=10, b=20)
```

Result:

```text
30
```

So:

```text
**args
```

is simply a **Python feature for passing dictionary values as function arguments**.

---

# 4. `ToolNode` — LangGraph

`ToolNode` is used inside LangGraph.

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode([add])
```

Now LangGraph can execute the tool when it receives a tool call from the LLM.

The flow becomes:

```text
User
 ↓
LLM
 ↓
Tool Call
 ↓
ToolNode
 ↓
add()
 ↓
Result
```

---

# 🔥 All Together

A typical LangGraph tool workflow looks like:

```python
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode


@tool
def add(a: int, b: int):
    """Add two numbers."""
    return a + b


llm = ChatGroq(
    model="openai/gpt-oss-20b"
)

llm_with_tools = llm.bind_tools([add])

tool_node = ToolNode([add])
```

The responsibilities are:

```text
@tool
  ↓
Create Tool

bind_tools()
  ↓
Give Tool to LLM

LLM
  ↓
Decides whether to call Tool

ToolNode
  ↓
Executes Tool
```

---

# ⚡ Without `@tool`

You can also use a normal Python function:

```python
def add(a, b):
    return a + b
```

Then:

```python
llm_with_tools = llm.bind_tools([add])
```

And with a normal Python call:

```python
args = {
    "a": 2,
    "b": 3
}

result = add(**args)
```

Output:

```text
5
```

However, if you want to use:

```python
add.invoke(...)
```

then `add` needs to be a LangChain Tool, such as one created with `@tool`.

---

# 🧠 Quick Cheat Sheet

| Concept        | What it does                           |
| -------------- | -------------------------------------- |
| `def add()`    | Normal Python function                 |
| `@tool`        | Converts function into LangChain Tool  |
| `bind_tools()` | Gives tools to the LLM                 |
| `**args`       | Python dictionary → function arguments |
| `ToolNode`     | Executes tools inside LangGraph        |
| `add.invoke()` | Executes a LangChain Tool              |

### Remember:

```text
             @tool
               ↓
        LangChain Tool
               ↓
        bind_tools()
               ↓
              LLM
               ↓
          Tool Call
               ↓
           ToolNode
               ↓
        Tool Execution
               ↓
             Result
```


> **`ToolNode` executes it in LangGraph.**
> **`**args` is just Python.**
