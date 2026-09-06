# 🦜 LangGraph Learning Roadmap

A beginner-friendly journey to understand **LangGraph** from the basics to **Multi-Agent Systems**.

This repository contains simple examples and practice code for learning how LangGraph works step-by-step.

---

## 🎯 Learning Roadmap

### 🟢 1. State

Understand what **State** is and why it is required in a LangGraph workflow.

> State = The shared data/memory that flows between different nodes.

---

### 🟢 2. Nodes

Learn how to create **Nodes** that perform specific tasks.

> Node = A function that does some work.

Example:

```text
Input → Node → Output
```

---

### 🟢 3. Edges

Learn how to connect nodes and define the workflow.

> Edge = Connection between two nodes.

```text
Node A → Node B → Node C
```

---

### 🟢 4. Messages

Understand how messages are passed between the user, LLM, and tools.

```text
User → Message → LLM → Response
```

---

### 🟢 5. Annotated + add_messages

Learn how LangGraph manages message state using:

* `Annotated`
* `add_messages`

This helps maintain and update conversation history.

---

### 🟢 6. LLM with Ollama

Connect a local LLM with LangGraph using **Ollama**.

```text
User
 ↓
LangGraph
 ↓
Ollama
 ↓
LLM
 ↓
Response
```

---

### 🟡 7. Conditional Edges

Learn how to make decisions inside a graph.

```text
          ┌──→ Node A
Input → Decision
          └──→ Node B
```

The next node depends on the current state.

---

### 🟡 8. Router

Learn how to create a **Router** that decides where the request should go.

```text
              ┌──→ Tool A
User → Router ├──→ Tool B
              └──→ LLM
```

---

## 🔵 Tool Calling & Agents

### 9. Tool Calling

Learn how an LLM can decide when it needs an external tool.

Examples:

* Calculator
* Search
* Weather
* Database
* Custom Python functions

```text
User → LLM → Tool → LLM → Response
```

---

### 10. ToolNode

Learn how LangGraph's `ToolNode` executes tools automatically.

```text
LLM
 ↓
Tool Call
 ↓
ToolNode
 ↓
Tool Result
```

---

### 11. LLM ↔ Tool Loop

Build a loop where the LLM can repeatedly call tools until it has enough information.

```text
       ┌──────────────┐
       ↓              │
User → LLM → Tool → Result
       ↑              │
       └──────────────┘
              ↓
           Final Answer
```

---

## 🤖 Agent Workflows

### 12. Agent Workflow

Combine:

* State
* Nodes
* Edges
* LLM
* Tools
* Conditional logic

to build an **AI Agent workflow**.

```text
User
 ↓
Agent
 ↓
Think
 ↓
Choose Tool
 ↓
Execute Tool
 ↓
Observe Result
 ↓
Final Answer
```

---

### 13. Memory / Checkpointing

Learn how to give agents **memory** using checkpointing.

This allows the graph to maintain state across interactions.

```text
Conversation 1
      ↓
  Checkpoint
      ↓
Conversation 2
      ↓
 Previous State
```

---

## 🔴 Multi-Agent Systems

### 14. Multiple Agents

Learn how multiple specialized agents can work together.

Example:

```text
             ┌→ Research Agent
User → Supervisor
             ├→ Coding Agent
             │
             └→ Writing Agent
```

Each agent performs a specific task.

---

### 15. Multi-Agent Architecture

Final step: build complete **Multi-Agent Systems**.

Learn architectures such as:

* Supervisor → Agents
* Agent → Agent
* Parallel Agents
* Sequential Agents
* Hierarchical Agents

Example:

```text
                    ┌→ Research Agent ──┐
                    │                   │
User → Supervisor ──┼→ Coding Agent ────┼→ Final Response
                    │                   │
                    └→ Review Agent ────┘
```

---

# 📚 Concepts Covered

| #  | Concept                  | Level           |
| -- | ------------------------ | --------------- |
| 1  | State                    | 🟢 Beginner     |
| 2  | Nodes                    | 🟢 Beginner     |
| 3  | Edges                    | 🟢 Beginner     |
| 4  | Messages                 | 🟢 Beginner     |
| 5  | Annotated + add_messages | 🟢 Beginner     |
| 6  | LLM + Ollama             | 🟢 Beginner     |
| 7  | Conditional Edges        | 🟡 Intermediate |
| 8  | Router                   | 🟡 Intermediate |
| 9  | Tool Calling             | 🟡 Intermediate |
| 10 | ToolNode                 | 🟡 Intermediate |
| 11 | LLM ↔ Tool Loop          | 🟡 Intermediate |
| 12 | Agent Workflow           | 🟡 Intermediate |
| 13 | Memory / Checkpointing   | 🟡 Intermediate |
| 14 | Multiple Agents          | 🔴 Advanced     |
| 15 | Multi-Agent Architecture | 🔴 Advanced     |

---

# 🛠️ Tech Stack

* 🐍 Python
* 🦜 LangGraph
* 🦜 LangChain
* 🧠 Ollama
* 🤖 LLMs
* 🔧 Tools & Tool Calling

---

# 📂 Repository Structure

```text
langgraph-learning/
│
├── 01_state/
├── 02_nodes/
├── 03_edges/
├── 04_messages/
├── 05_annotated_add_messages/
├── 06_llm_ollama/
├── 07_conditional_edges/
├── 08_router/
├── 09_tool_calling/
├── 10_tool_node/
├── 11_llm_tool_loop/
├── 12_agent_workflow/
├── 13_memory_checkpointing/
├── 14_multiple_agents/
├── 15_multi_agent_architecture/
│
└── README.md
```

---

# 🎯 Goal

The goal of this repository is to go from:

```text
Basic LangGraph Concepts
        ↓
LLM Integration
        ↓
Conditional Workflows
        ↓
Tool Calling
        ↓
Agents
        ↓
Memory
        ↓
Multiple Agents
        ↓
Multi-Agent Systems 🚀
```

---

## 🚀 Progress

* [ ] State
* [ ] Nodes
* [ ] Edges
* [ ] Messages
* [ ] Annotated + add_messages
* [ ] LLM with Ollama
* [ ] Conditional Edges
* [ ] Router
* [ ] Tool Calling
* [ ] ToolNode
* [ ] LLM ↔ Tool Loop
* [ ] Agent Workflow
* [ ] Memory / Checkpointing
* [ ] Multiple Agents
* [ ] Multi-Agent Architecture

---

### ⭐ Learning Philosophy

> **Learn → Build → Experiment → Break → Fix → Repeat.**

This repository is focused on **learning LangGraph by building small examples instead of only studying theory**.

