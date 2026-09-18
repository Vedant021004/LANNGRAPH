
## PS 1 — Customer Support Pipeline

**Concept:** Sequential + Structured Output

Ek customer ka complaint lo:

```text
"I ordered a laptop but it arrived damaged."
```

Workflow:

```text
START
  ↓
classify_complaint
  ↓
generate_response
  ↓
END
```

### Requirements

`classify_complaint` ko structured output dena hai:

```python
class Complaint(BaseModel):
    category: Literal["delivery", "product", "payment", "other"]
    priority: Literal["low", "medium", "high"]
```

Example:

```text
category → product
priority → high
```

Then `generate_response` us information ke basis par customer ko response generate kare.

**Practice:** `ChatPromptTemplate`, Pydantic, sequential edges.

---

# PS 2 — AI Research Assistant

**Concept:** Parallel

User:

```text
"Explain electric vehicles."
```

Ek saath 3 independent tasks perform karo:

```text
                  START
                    ↓
                  PARALLEL
              ↙      ↓       ↘
         definition  benefits  drawbacks
              ↘       ↓       ↙
                 combine
                    ↓
                   END
```

### Requirements

Teen nodes:

```python
get_definition()
get_benefits()
get_drawbacks()
```

Ye **parallel** run hone chahiye.

Then ek `combine` node teeno outputs ko combine kare.

### State

Tumhe khud decide karna hai ki state mein kya fields chahiye.

Hint:

```python
class State(TypedDict):
    topic: str
    definition: str
    benefits: str
    drawbacks: str
    final_answer: str
```

**Practice:** Parallel execution + State + reducer/combination.

---

# PS 3 — Smart Query Router

**Concept:** Structured Output + Conditional Routing

User kuch bhi pooch sakta hai:

```text
"What is Python?"
"What's the weather?"
"Book a meeting tomorrow."
"Calculate 25 * 40."
```

Workflow:

```text
                 START
                   ↓
                CLASSIFY
                   ↓
          ┌────────┼────────┐
          ↓        ↓        ↓
       general   weather  calendar
          ↓        ↓        ↓
          └────────┼────────┘
                   ↓
                  END
```

Classifier ka structured output:

```python
class QueryType(BaseModel):
    intent: Literal[
        "general",
        "weather",
        "calendar"
    ]
```

Router:

```python
def router(state):
    if state["intent"] == "general":
        return "general"

    elif state["intent"] == "weather":
        return "weather"

    return "calendar"
```

### Challenge

LLM ko **router directly control nahi karna hai**.

LLM → structured result
Python → routing decision.

**Practice:** `Literal`, `with_structured_output()`, conditional edges.

---

# PS 4 — AI Answer Quality Checker

**Concept:** Looping + Structured Output

Ye tumhare sir ke diagram jaisa hai. 🔥

User:

```text
"Explain neural networks."
```

Workflow:

```text
START
  ↓
GENERATE
  ↓
EVALUATE
  ↓
 ┌───────────────┐
 ↓               ↓
APPROVED    NEEDS_IMPROVEMENT
 ↓               ↓
END           OPTIMIZE
                 ↓
              GENERATE
                 ↓
              EVALUATE
                 ↺
```

Evaluator schema:

```python
class Evaluation(BaseModel):
    status: Literal[
        "approved",
        "needs_improvement"
    ]
    score: int
    feedback: str
```

### Important condition

Maximum **3 attempts** allowed.

So State mein:

```python
class State(TypedDict):
    task: str
    answer: str
    score: int
    feedback: str
    status: str
    attempts: int
```

Router ko check karna hai:

```text
approved
    ↓
END

needs_improvement + attempts < 3
    ↓
OPTIMIZE

attempts >= 3
    ↓
END
```

**Practice:** Loop + conditional routing + structured output + state updates.

---

# PS 5 — AI Content Creation Pipeline 🚀

**Concept:** Sequential + Parallel + Conditional + Loop + Structured Output

Ab sab concepts **ek hi project** mein use karo.

User:

```text
"Create a LinkedIn post about RAG."
```

Workflow design karo:

```text
                         START
                           ↓
                      CLASSIFIER
                           ↓
                        GENERATE
                           ↓
                     ┌─────┴─────┐
                     ↓           ↓
                 TECHNICAL    EXAMPLE
                     ↓           ↓
                     └─────┬─────┘
                           ↓
                        EVALUATE
                           ↓
                    ┌──────┴──────┐
                    ↓             ↓
                APPROVED    NEEDS_IMPROVEMENT
                    ↓             ↓
                   END         OPTIMIZE
                                  ↓
                               GENERATE
                                  ↺
```

### Classifier

Structured output:

```python
class ContentRequest(BaseModel):
    topic: str
    audience: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ]
    platform: Literal[
        "linkedin",
        "twitter",
        "blog"
    ]
```

### Evaluator

```python
class Evaluation(BaseModel):
    score: int
    status: Literal[
        "approved",
        "needs_improvement"
    ]
    feedback: str
```

### Parallel nodes

```text
GENERATE
   ↓
┌──────────────┐
↓              ↓
TECHNICAL    EXAMPLE
↓              ↓
└──────┬───────┘
       ↓
   COMBINE
       ↓
   EVALUATE
```

### Loop

```text
EVALUATE
   ↓
score >= 8 → END

score < 8
   ↓
OPTIMIZE
   ↓
GENERATE
   ↓
EVALUATE
```

---

## 🔥 Difficulty order

| PS | Main Concept                           | Difficulty |
| -- | -------------------------------------- | ---------- |
| 1  | Sequential + Structured Output         | ⭐          |
| 2  | Parallel                               | ⭐⭐         |
| 3  | Conditional + Structured Output        | ⭐⭐         |
| 4  | Loop + Conditional + Structured Output | ⭐⭐⭐⭐       |
| 5  | **Everything together**                | ⭐⭐⭐⭐⭐      |

### One rule while solving

**Pehle khud architecture draw karna. Code baad mein.**

Har problem ke liye pehle ye 4 cheezein likho:

```text
1. State mein kya chahiye?
2. Kaunse nodes chahiye?
3. Kaunse edges normal hain?
4. Kahan conditional / parallel / loop chahiye?
```

Phir code likho.

**PS 1 se start karo aur mujhe apna code bhejo — main sirf bugs/hints dunga, pura solution nahi**, taaki actual practice ho. 🔥
