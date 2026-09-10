# LangGraph: Messages, Tools, Agents & Routing — Complete Mental Model

This README explains the relationship between:

* `BaseModel`
* `MessagesState`
* `HumanMessage`
* `AIMessage`
* `SystemMessage`
* `ToolMessage`
* `ChatPromptTemplate`
* Normal Python functions
* `@tool`
* `bind_tools()`
* `ToolNode`
* Classifiers
* Routers
* Agents
* `create_agent()`
* `create_react_agent()`

The goal is **not to memorize APIs**.

The goal is to understand:

> **What problem are we solving? → What do we need? → Why do we need it? → What can replace what?**

---

# 1. The Big Picture

A basic LLM application looks like:

```text
User
  ↓
LLM
  ↓
Answer
```

But real applications become more complicated:

```text
User
  ↓
Understand the request
  ↓
Decide what to do
  ↓
Maybe call a tool
  ↓
Get tool result
  ↓
Think again
  ↓
Final answer
```

LangGraph and LangChain provide different abstractions for building these systems.

---

# 2. First Understand the Difference: State vs Message

This is one of the most important concepts.

## Message

A message is one individual piece of conversation.

Examples:

```text
HumanMessage
AIMessage
SystemMessage
ToolMessage
```

Example:

```python
HumanMessage(content="What is LangGraph?")
```

This represents:

```text
USER:
What is LangGraph?
```

---

## State

State is the information currently carried through the graph.

Example:

```python
class State(BaseModel):
    question: str
    route: str
    answer: str
```

The graph can pass this state from node to node.

```text
START
  ↓
Classifier
  ↓
Tool
  ↓
LLM
  ↓
END
```

Each node can read and update the state.

---

# 3. `BaseModel`

`BaseModel` comes from Pydantic.

```python
from pydantic import BaseModel
```

It is a **generic way to define structured data**.

Example:

```python
class State(BaseModel):
    question: str
    route: str = ""
    answer: str = ""
```

Now your state is:

```text
State
├── question
├── route
└── answer
```

## Why use it?

Because your graph may need information other than messages.

For example:

```python
class State(BaseModel):
    question: str
    route: str
    user_name: str
    score: int
    answer: str
```

`BaseModel` gives you a flexible structure.

---

# 4. `MessagesState`

LangGraph provides:

```python
from langgraph.graph import MessagesState
```

`MessagesState` is a **ready-made state schema specifically designed for message-based graphs**.

Instead of manually defining:

```python
class State(BaseModel):
    messages: Annotated[list, add_messages]
```

you can use:

```python
class State(MessagesState):
    pass
```

Or add your own fields:

```python
class State(MessagesState):
    next_agent: str
```

Conceptually:

```text
MessagesState
├── messages
└── message merging behavior

        ↓ inherit

State
├── messages
└── next_agent
```

---

# 5. Does `MessagesState` Replace `BaseModel`?

Not completely.

Think of it like this:

```text
BaseModel
   ↓
Generic structured state

MessagesState
   ↓
Ready-made message-oriented state
```

### Use `BaseModel` when:

Your state contains many custom fields:

```python
class State(BaseModel):
    question: str
    route: str
    answer: str
```

### Use `MessagesState` when:

Your graph mainly revolves around conversation:

```python
class State(MessagesState):
    user_name: str
```

---

# 6. `HumanMessage`

```python
from langchain_core.messages import HumanMessage
```

Represents a message from the user.

```python
HumanMessage(
    content="Explain LangGraph."
)
```

Conceptually:

```text
USER
 ↓
"Explain LangGraph."
```

---

# 7. `AIMessage`

```python
from langchain_core.messages import AIMessage
```

Represents a message produced by the AI.

Example:

```python
AIMessage(
    content="LangGraph is a framework..."
)
```

Usually you don't manually create this.

When you do:

```python
response = llm.invoke(...)
```

the response is generally an `AIMessage`.

---

# 8. `SystemMessage`

```python
from langchain_core.messages import SystemMessage
```

Represents instructions given to the model.

Example:

```python
SystemMessage(
    content="You are a helpful Python teacher."
)
```

The model sees:

```text
SYSTEM:
You are a helpful Python teacher.

USER:
Explain lists.
```

---

# 9. `ToolMessage`

Another important message type:

```python
ToolMessage
```

It represents the result returned by a tool.

A tool-calling conversation can look like:

```text
HumanMessage
      ↓
User asks something

AIMessage
      ↓
LLM requests a tool

ToolMessage
      ↓
Tool returns result

AIMessage
      ↓
LLM produces final answer
```

---

# 10. Do We Always Need `HumanMessage`, `AIMessage`, `SystemMessage`?

No.

This is where `ChatPromptTemplate` becomes useful.

---

# 11. `ChatPromptTemplate`

```python
from langchain_core.prompts import ChatPromptTemplate
```

Instead of manually creating:

```python
SystemMessage(...)
HumanMessage(...)
```

you can define a reusable template:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful Python teacher."),
    ("human", "{question}")
])
```

Then:

```python
prompt.invoke({
    "question": "What is a list?"
})
```

creates the structured prompt.

---

# 12. What Does `ChatPromptTemplate` Replace?

For **prompt construction**, it can replace the need to manually create:

```python
SystemMessage
HumanMessage
```

Instead of:

```python
messages = [
    SystemMessage(content="You are a teacher."),
    HumanMessage(content="Explain {topic}")
]
```

you can write:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a teacher."),
    ("human", "Explain {topic}")
])
```

But:

> `ChatPromptTemplate` does NOT make message classes obsolete.

It is a **template for producing structured messages**.

---

# 13. Important Comparison

```text
HumanMessage
    ↓
One actual user message

AIMessage
    ↓
One actual AI message

SystemMessage
    ↓
One actual system instruction

ToolMessage
    ↓
One actual tool result

ChatPromptTemplate
    ↓
A reusable template for creating messages
```

---

# 14. Normal Python Function

Suppose you create:

```python
def addition(a, b):
    return a + b
```

This is a normal Python function.

Python code can call it:

```python
addition(10, 20)
```

Flow:

```text
Python
  ↓
addition()
  ↓
30
```

The LLM does not automatically know that this function exists.

---

# 15. Why Convert a Function into a Tool?

Use:

```python
from langchain_core.tools import tool

@tool
def addition(a: int, b: int):
    """Add two numbers."""
    return a + b
```

Now the function becomes a **tool that can be exposed to an LLM/agent**.

The model can receive information such as:

```text
Tool name:
addition

Description:
Add two numbers.

Arguments:
a: integer
b: integer
```

This allows the model to decide:

```text
User:
What is 25 + 37?

        ↓

LLM:
I should use addition.

        ↓

addition(25, 37)

        ↓

62
```

---

# 16. Function vs Tool

This distinction is extremely important.

## Normal Function

```python
def addition(a, b):
    return a + b
```

Means:

> Python can execute this function.

---

## Tool

```python
@tool
def addition(a: int, b: int):
    """Add two numbers."""
    return a + b
```

Means:

> Python can execute this function AND an LLM/agent can be given its structured description so it can request the tool.

---

# 17. Does Every Function Need to Become a Tool?

No.

If your program already knows exactly when to call the function:

```python
if route == "addition":
    addition(...)
```

there is no need for tool calling.

Example:

```text
User
 ↓
Classifier
 ↓
"addition"
 ↓
Python function
 ↓
Answer
```

This is perfectly valid.

---

# 18. Classifier

A classifier answers:

> **What kind of request is this?**

Example:

```text
User:
"What is 20 + 30?"

        ↓

Classifier

        ↓

addition
```

Possible categories:

```text
tavily
addition
llm
```

---

# 19. Router

A router answers:

> **Where should this request go?**

Example:

```text
Classifier
    ↓
addition
    ↓
Addition Node
```

The classifier may determine the category, while the router uses that decision to select the graph path.

---

# 20. Your Manual Architecture

You can build:

```text
                  USER
                    ↓
               CLASSIFIER
                    ↓
                  ROUTER
          ┌─────────┼─────────┐
          ↓         ↓         ↓
       Tavily    Addition     LLM
          ↓         ↓         ↓
         END       END       END
```

No tools are required.

No agent is required.

Normal Python functions are enough.

This is a **deterministic workflow**.

---

# 21. Why Use an Agent?

An agent becomes useful when you don't want to manually define every decision.

Instead of:

```text
If addition → addition
If search → search
If weather → weather
```

you can give the LLM several tools:

```text
Agent
 ├── calculator
 ├── search
 ├── weather
 └── database
```

The LLM decides what to use.

```text
User
 ↓
Agent
 ↓
What action should I take?
 ↓
Tool
 ↓
Result
 ↓
Do I need another action?
 ↓
...
 ↓
Final answer
```

---

# 22. `bind_tools()`

```python
llm_with_tools = llm.bind_tools([
    addition
])
```

This tells the LLM:

> **These tools are available to you.**

It does NOT mean that the tool has already executed.

Think:

```text
bind_tools()
     ↓
Tell LLM about available capabilities
```

---

# 23. `ToolNode`

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode([addition])
```

`ToolNode` is a LangGraph node that **executes tool calls**.

Flow:

```text
LLM
 ↓
Tool call
 ↓
ToolNode
 ↓
addition()
 ↓
Tool result
 ↓
LLM
```

---

# 24. `bind_tools()` vs `ToolNode`

This is one of the most important differences.

```text
bind_tools()
     ↓
LLM knows what tools it can request
```

```text
ToolNode()
     ↓
LangGraph executes the requested tool
```

### Memory trick

> `bind_tools()` = **Show the menu**

> `ToolNode` = **Prepare the ordered item**

---

# 25. Manual Tool-Calling Architecture

You can build:

```text
                 START
                   ↓
                  LLM
                   ↓
             Tool required?
              ↙          ↘
            YES           NO
             ↓             ↓
         ToolNode         END
             ↓
        Tool result
             ↓
            LLM
```

This gives you more control.

---

# 26. ReAct Agent

ReAct means:

```text
Reason + Act
```

The basic idea is:

```text
Think about task
      ↓
Take action
      ↓
Observe result
      ↓
Think again
      ↓
Take another action if needed
      ↓
Final answer
```

For example:

```text
User
 ↓
Agent
 ↓
Search tool
 ↓
Search result
 ↓
Agent
 ↓
Calculator
 ↓
Result
 ↓
Agent
 ↓
Final answer
```

---

# 27. `create_react_agent()`

LangGraph provides a prebuilt ReAct-style agent API in versions that support it:

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=llm,
    tools=[addition]
)
```

Instead of manually creating:

```text
LLM node
ToolNode
Conditional edges
Loop
```

you use the prebuilt agent.

---

# 28. `create_agent()`

LangChain provides a higher-level agent API:

```python
from langchain.agents import create_agent

agent = create_agent(
    model=llm,
    tools=[addition]
)
```

This lets you create an agent without manually constructing the graph.

For newer LangChain applications, `create_agent()` is generally the preferred high-level API.

---

# 29. `create_agent()` vs `create_react_agent()`

Conceptually:

```text
create_agent()
      ↓
Modern high-level LangChain agent API
```

while:

```text
create_react_agent()
      ↓
Prebuilt LangGraph ReAct-style workflow
```

The exact API behavior depends on the installed LangChain/LangGraph version.

---

# 30. What Replaces What?

This is the section to remember.

## State

```text
BaseModel
   ↓
Use when you want custom state

MessagesState
   ↓
Use when your state is primarily messages
```

`MessagesState` does not replace `BaseModel` for every situation.

---

## Messages

```text
HumanMessage
AIMessage
SystemMessage
ToolMessage
```

These represent **actual messages**.

While:

```text
ChatPromptTemplate
```

is a **template used to construct structured prompts/messages**.

For prompt construction:

```text
Manual Message Objects
        ↓
Can often be replaced by
        ↓
ChatPromptTemplate
```

---

## Functions and Tools

```text
Normal Function
        ↓
Python decides when to call it
```

```text
@tool
        ↓
LLM/Agent can be given the function as a tool
```

A normal function does not need to become a tool unless you want LLM-driven tool calling.

---

## Tool Calling

Manual:

```text
bind_tools()
+
ToolNode()
+
Graph edges
+
Conditional logic
```

Higher-level:

```text
create_agent()
```

or, depending on API/version:

```text
create_react_agent()
```

---

# 31. The Complete Abstraction Ladder

Think of LangGraph/LangChain as different levels of abstraction.

```text
LEVEL 1 — Raw Python
─────────────────────

Function
    ↓
Python calls function


LEVEL 2 — LangGraph
─────────────────────

State
 ↓
Nodes
 ↓
Edges
 ↓
Conditional routing


LEVEL 3 — Tool Calling
─────────────────────

LLM
 ↓
bind_tools()
 ↓
ToolNode
 ↓
Tool
 ↓
LLM


LEVEL 4 — Agent
─────────────────────

Agent
 ↓
LLM
 ↓
Choose tool
 ↓
Execute
 ↓
Observe
 ↓
Choose next action
 ↓
Final answer


LEVEL 5 — High-Level Agent API
───────────────────────────────

create_agent()
```

---

# 32. When Should You Use What?

## Use a normal function when:

The program already knows what to do.

```python
if route == "addition":
    addition(...)
```

---

## Use a classifier/router when:

You have a known set of paths.

```text
Coding
Search
Math
General
```

and you want predictable control.

---

## Use `MessagesState` when:

Your graph mainly works with conversation messages.

```python
class State(MessagesState):
    next_agent: str
```

---

## Use `BaseModel` when:

You need custom structured state.

```python
class State(BaseModel):
    question: str
    route: str
    score: int
    answer: str
```

---

## Use `ChatPromptTemplate` when:

You want reusable, structured prompts.

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a teacher."),
    ("human", "{question}")
])
```

---

## Use `@tool` when:

You want to expose a Python capability to an LLM/agent.

```python
@tool
def search(...):
    ...
```

---

## Use `bind_tools()` when:

You are manually building a tool-calling workflow and need to tell the LLM about available tools.

```python
llm.bind_tools(tools)
```

---

## Use `ToolNode` when:

You are building a LangGraph tool-calling loop manually and need a node that executes tool calls.

```python
ToolNode(tools)
```

---

## Use an Agent when:

The task requires dynamic decision-making.

```text
Which tool?
 ↓
Do I need another tool?
 ↓
What should I do next?
```

---

# 33. The Most Important Architecture Comparison

## A. Deterministic Routing

```text
                 User
                   ↓
              Classifier
                   ↓
                Router
          ┌────────┼────────┐
          ↓        ↓        ↓
        Math     Search    General
          ↓        ↓        ↓
        END      END      END
```

**You control the path.**

---

## B. Manual Tool Calling

```text
                 User
                   ↓
                  LLM
                   ↓
             Tool required?
              ↙          ↘
            YES           NO
             ↓             ↓
         ToolNode         END
             ↓
         Tool result
             ↓
             LLM
```

**You control the graph, while the LLM chooses tools.**

---

## C. Agent

```text
                 User
                   ↓
                 Agent
                   ↓
            LLM decides action
                   ↓
                 Tool
                   ↓
                Result
                   ↓
                 Agent
                   ↓
           Another action?
             ↙          ↘
           YES           NO
            ↓             ↓
          Tool          Answer
            ↓
           ...
```

**The agent controls the decision loop dynamically.**

---

# 34. Can an Agent Replace a Classifier?

Sometimes.

For example:

```text
Classifier:
"What category is this?"

Agent:
"What should I do to solve this?"
```

If you have only a few known routes:

```text
Math
Search
Coding
```

a classifier/router can be better because it is predictable.

If the task is open-ended:

```text
Search
 ↓
Read
 ↓
Calculate
 ↓
Search again
 ↓
Compare
 ↓
Answer
```

an agent is often more suitable.

---

# 35. Can We Use Both?

Absolutely.

A powerful architecture can be:

```text
                       USER
                         ↓
                    SUPERVISOR
                         ↓
          ┌──────────────┼──────────────┐
          ↓              ↓              ↓
      Research         Coding          SQL
        Agent           Agent          Agent
          ↓              ↓              ↓
       Tools           Tools          Tools
          ↓              ↓              ↓
          └──────────────┼──────────────┘
                         ↓
                    FINAL ANSWER
```

Here:

```text
Supervisor
    ↓
High-level routing

Agent
    ↓
Low-level dynamic decision-making

Tools
    ↓
Actual external capabilities
```

---

# 36. Final Mental Model

Remember these questions.

### Question 1:

> **Where should the request go?**

Use:

```text
Classifier / Router
```

---

### Question 2:

> **What information is being carried through my graph?**

Use:

```text
State
```

or:

```text
MessagesState
```

---

### Question 3:

> **What kind of message is this?**

Use:

```text
HumanMessage
AIMessage
SystemMessage
ToolMessage
```

---

### Question 4:

> **How should I construct a reusable prompt?**

Use:

```text
ChatPromptTemplate
```

---

### Question 5:

> **I have a Python function that I want an LLM to use.**

Use:

```text
@tool
```

---

### Question 6:

> **I manually want the LLM to have access to these tools.**

Use:

```text
bind_tools()
```

---

### Question 7:

> **I manually built a LangGraph and need to execute tool calls.**

Use:

```text
ToolNode
```

---

### Question 8:

> **I don't want to manually build the tool-calling decision loop.**

Use:

```text
Agent
```

such as:

```text
create_agent()
```

or an appropriate ReAct/prebuilt API for your installed version.

---

# 37. One Final Diagram

```text
                         USER
                           │
                           ↓
                    ┌─────────────┐
                    │    STATE    │
                    └──────┬──────┘
                           │
                           ↓
                  ┌─────────────────┐
                  │ Classifier /    │
                  │ Router          │
                  └────────┬────────┘
                           │
              ┌────────────┼────────────┐
              ↓            ↓            ↓
           Function      Agent        LLM
                           │
                           ↓
                         Tools
                           │
                ┌──────────┴──────────┐
                ↓                     ↓
          bind_tools()            ToolNode
                │                     │
                ↓                     ↓
           LLM knows              Tool executes
           the tools              the tool
```

---

# 38. The Golden Rule

Don't choose an abstraction just because it is shorter.

Choose it based on **who should make the decision**.

```text
Python decides
    ↓
Normal function / deterministic graph


Classifier decides
    ↓
Router


LLM decides
    ↓
Tool calling / Agent


Agent decides repeatedly
    ↓
Dynamic multi-step workflow
```

That is the core mental model behind everything in this README.
