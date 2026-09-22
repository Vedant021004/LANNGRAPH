Bilkul! 🔥 Main tumhare liye Conditional Edge ka complete workflow README bana raha hoon — especially is tarah ki tumhe State → Classifier → Router → Conditional Edge → Next Node → State Update ka flow permanently clear ho jaye.

🔀 LangGraph Conditional Edges — Complete Workflow

1. What is a Conditional Edge?

A conditional edge in LangGraph is used when the next node should be selected dynamically based on the current state.

Normal edge:

START
  ↓
Node A
  ↓
Node B
  ↓
END

The next node is fixed.

Conditional edge:

START
  ↓
Node A
  ↓
Decision
  ├──→ Node B
  ├──→ Node C
  └──→ Node D

The next node depends on a condition.

⸻

2. The Core Workflow

The most important workflow is:

User Input
    ↓
State
    ↓
Classifier
    ↓
State Update
    ↓
Router
    ↓
Routing Decision
    ↓
Conditional Edge Mapping
    ↓
Selected Node
    ↓
State Update
    ↓
END

Remember:

Classifier = What type is this?
State = Store the result.
Router = Read the result and tell LangGraph where to go.
Conditional Edge = Map that decision to an actual node.

⸻

3. Complete Example

We will build a simple system that handles:

Python questions
SQL questions
General questions

⸻

4. Step 1 — Define State

from typing import TypedDict
class State(TypedDict):
    question: str
    question_type: str
    answer: str

Our state contains three pieces of information:

question
question_type
answer

Think of state as a shared container.

Initially:

{
    "question": "How do I learn Python?",
    "question_type": "",
    "answer": ""
}

⸻

5. Step 2 — Classifier Node

The classifier analyzes the question.

def classifier(state: State):
    question = state["question"].lower()
    if "python" in question:
        return {
            "question_type": "python"
        }
    elif "sql" in question:
        return {
            "question_type": "sql"
        }
    else:
        return {
            "question_type": "general"
        }

The classifier does not select the next graph node.

Its job is:

Analyze question
      ↓
Determine category
      ↓
Update state

For example:

Input:
"How do I learn Python?"

Classifier returns:

{
    "question_type": "python"
}

State becomes:

{
    "question": "How do I learn Python?",
    "question_type": "python",
    "answer": ""
}

⸻

6. Step 3 — Router

Now we create the router.

def route_question(state: State):
    return state["question_type"]

This function is very simple.

It does not update the state.

It only reads:

state["question_type"]

For example:

state["question_type"]

returns:

"python"

So the router returns:

"python"

⸻

7. What Exactly Does the Router Do?

This is the most important concept.

The router does:

STATE
  ↓
Read question_type
  ↓
"python"

It does NOT do:

STATE
  ↓
Update question_type

The classifier does that.

Therefore:

Classifier → writes/updates information
Router → reads information and returns a routing decision

⸻

8. Step 4 — Create Nodes

Now create the actual nodes.

def python_node(state: State):
    return {
        "answer": "This is a Python question."
    }
def sql_node(state: State):
    return {
        "answer": "This is an SQL question."
    }
def general_node(state: State):
    return {
        "answer": "This is a general question."
    }

These nodes perform the actual work.

⸻

9. Step 5 — Create the Graph

from langgraph.graph import StateGraph, START, END
builder = StateGraph(State)

⸻

10. Add Nodes

builder.add_node("classifier", classifier)
builder.add_node("python_node", python_node)
builder.add_node("sql_node", sql_node)
builder.add_node("general_node", general_node)

The graph now contains:

classifier
python_node
sql_node
general_node

⸻

11. Connect START to Classifier

builder.add_edge(
    START,
    "classifier"
)

Flow:

START
  ↓
classifier

⸻

12. The Important Part — Conditional Edge

Now:

builder.add_conditional_edges(
    "classifier",
    route_question,
    {
        "python": "python_node",
        "sql": "sql_node",
        "general": "general_node"
    }
)

Let’s break this down.

⸻

Argument 1 — "classifier"

"classifier"

This means:

Start conditional routing after the classifier node.

Flow:

START
  ↓
classifier
  ↓
???

⸻

Argument 2 — route_question

route_question

This means:

Call this function to determine the routing decision.

LangGraph effectively does:

decision = route_question(state)

Suppose:

decision = "python"

⸻

Argument 3 — Mapping

{
    "python": "python_node",
    "sql": "sql_node",
    "general": "general_node"
}

This maps the router’s result to an actual graph node.

Router result       Actual node
"python"     →      python_node
"sql"        →      sql_node
"general"   →       general_node

⸻

13. Complete Flow

Suppose user asks:

How do I learn Python?

Step 1

Initial state:

{
    "question": "How do I learn Python?",
    "question_type": "",
    "answer": ""
}

⸻

Step 2

Classifier executes:

classifier

It checks:

if "python" in question:

True.

It returns:

{
    "question_type": "python"
}

⸻

Step 3

State updates:

{
    "question": "How do I learn Python?",
    "question_type": "python",
    "answer": ""
}

⸻

Step 4

Router executes:

route_question(state)

It reads:

state["question_type"]

Result:

"python"

⸻

Step 5

LangGraph checks the mapping:

{
    "python": "python_node",
    "sql": "sql_node",
    "general": "general_node"
}

It finds:

"python" → "python_node"

⸻

Step 6

LangGraph executes:

python_node

It returns:

{
    "answer": "This is a Python question."
}

⸻

Step 7

State becomes:

{
    "question": "How do I learn Python?",
    "question_type": "python",
    "answer": "This is a Python question."
}

⸻

Step 8

Graph reaches:

END

⸻

14. Complete Visual Workflow

                         USER
                           │
                           │
                           ▼
                    "Learn Python"
                           │
                           ▼
                    ┌────────────┐
                    │   STATE    │
                    │            │
                    │ question   │
                    │ type = ""   │
                    │ answer = "" │
                    └──────┬─────┘
                           │
                           ▼
                    ┌────────────┐
                    │ CLASSIFIER │
                    └──────┬─────┘
                           │
                           │ analyzes question
                           ▼
                    question_type
                       = python
                           │
                           ▼
                    ┌────────────┐
                    │    STATE   │
                    │            │
                    │ type=python│
                    └──────┬─────┘
                           │
                           ▼
                    ┌────────────┐
                    │   ROUTER   │
                    └──────┬─────┘
                           │
                           │ reads state
                           ▼
                       "python"
                           │
                           ▼
               ┌─────────────────────┐
               │ CONDITIONAL EDGE    │
               │                     │
               │ python → python_node│
               │ sql → sql_node      │
               │ general → general   │
               └──────────┬──────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ python_node │
                   └──────┬──────┘
                          │
                          │ updates answer
                          ▼
                    ┌──────────┐
                    │  STATE   │
                    │          │
                    │ type=python
                    │ answer=...
                    └────┬─────┘
                         │
                         ▼
                        END

⸻

15. What Does Each Component Do?

Component	Responsibility
State	Stores shared graph data
classifier	Analyzes input
Classifier output	Updates state
route_question	Reads state
Router output	Routing decision
Conditional edge	Maps decision → node
python_node	Performs actual work
Node output	Updates state
END	Finishes workflow

⸻

16. Classifier vs Router

This is the most important distinction.

Classifier

def classifier(state):
    return {
        "question_type": "python"
    }

Its job:

Question
   ↓
Analyze
   ↓
Category
   ↓
State Update

⸻

Router

def route_question(state):
    return state["question_type"]

Its job:

State
   ↓
Read category
   ↓
Return routing decision

It does NOT update:

question_type

⸻

17. Conditional Edge Is the Bridge

Think of the router and conditional edge together:

Router
  ↓
"python"
  ↓
Conditional Edge
  ↓
"python_node"

The router says:

“My decision is Python.”

The conditional edge says:

“Okay, Python means python_node.”

⸻

18. Why Not Just Make the Classifier Return "python_node"?

You could technically design routing that way, but separating the concepts makes complex workflows easier to maintain.

Instead of:

def classifier(state):
    return "python_node"

we use:

def classifier(state):
    return {
        "question_type": "python"
    }

Then:

def route_question(state):
    return state["question_type"]

This keeps the state meaningful.

Your state tells you:

question_type = python

rather than:

next_node = python_node

This becomes particularly useful when the same state is used by multiple nodes.

⸻

19. Full Code

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
# =========================
# STATE
# =========================
class State(TypedDict):
    question: str
    question_type: str
    answer: str
# =========================
# CLASSIFIER
# =========================
def classifier(state: State):
    question = state["question"].lower()
    if "python" in question:
        return {
            "question_type": "python"
        }
    elif "sql" in question:
        return {
            "question_type": "sql"
        }
    else:
        return {
            "question_type": "general"
        }
# =========================
# ROUTER
# =========================
def route_question(state: State):
    return state["question_type"]
# =========================
# PYTHON NODE
# =========================
def python_node(state: State):
    return {
        "answer": "This is a Python question."
    }
# =========================
# SQL NODE
# =========================
def sql_node(state: State):
    return {
        "answer": "This is an SQL question."
    }
# =========================
# GENERAL NODE
# =========================
def general_node(state: State):
    return {
        "answer": "This is a general question."
    }
# =========================
# BUILD GRAPH
# =========================
builder = StateGraph(State)
builder.add_node(
    "classifier",
    classifier
)
builder.add_node(
    "python_node",
    python_node
)
builder.add_node(
    "sql_node",
    sql_node
)
builder.add_node(
    "general_node",
    general_node
)
# =========================
# START
# =========================
builder.add_edge(
    START,
    "classifier"
)
# =========================
# CONDITIONAL EDGE
# =========================
builder.add_conditional_edges(
    "classifier",
    route_question,
    {
        "python": "python_node",
        "sql": "sql_node",
        "general": "general_node"
    }
)
# =========================
# END
# =========================
builder.add_edge(
    "python_node",
    END
)
builder.add_edge(
    "sql_node",
    END
)
builder.add_edge(
    "general_node",
    END
)
# =========================
# COMPILE
# =========================
graph = builder.compile()
# =========================
# RUN
# =========================
question = input("Ask: ")
result = graph.invoke({
    "question": question,
    "question_type": "",
    "answer": ""
})
print("\nFinal State:")
print(result)

⸻

20. Test Cases

Test 1

Input:

How do I learn Python?

Flow:

classifier
    ↓
question_type = python
    ↓
router
    ↓
"python"
    ↓
python_node
    ↓
END

⸻

Test 2

Input:

How do I create a SQL table?

Flow:

classifier
    ↓
question_type = sql
    ↓
router
    ↓
"sql"
    ↓
sql_node
    ↓
END

⸻

Test 3

Input:

What is machine learning?

Flow:

classifier
    ↓
question_type = general
    ↓
router
    ↓
"general"
    ↓
general_node
    ↓
END

⸻

21. The One Diagram You Should Remember

                    USER INPUT
                        │
                        ▼
                   ┌──────────┐
                   │ CLASSIFIER│
                   └─────┬────┘
                         │
                         │ updates
                         ▼
                       STATE
                         │
                  type = "python"
                         │
                         │ reads
                         ▼
                    ┌─────────┐
                    │ ROUTER  │
                    └────┬────┘
                         │
                         │ returns
                         ▼
                      "python"
                         │
                         ▼
                CONDITIONAL EDGE
                         │
                         │ mapping
                         ▼
                   python_node
                         │
                         ▼
                       STATE
                         │
                         ▼
                        END

Final Mental Model

Classifier:
"Is this Python, SQL, or General?"
        ↓
State:
"question_type = python"
        ↓
Router:
"I read question_type.
It says python."
        ↓
Conditional Edge:
"python means python_node."
        ↓
python_node:
"Now I'll actually perform the Python-related work."

In one sentence:

Classifier state mein decision save karta hai → Router us decision ko read karke return karta hai → Conditional Edge us returned value ko actual next node se map karta hai → next node execute hota hai.