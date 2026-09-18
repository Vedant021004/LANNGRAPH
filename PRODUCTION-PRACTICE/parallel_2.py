from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
import operator

load_dotenv()


# =========================
# LLM
# =========================

model = ChatGroq(
    model="openai/gpt-oss-20b",
    
)


# =========================
# STRUCTURED OUTPUT
# =========================

class EvaluationSchema(BaseModel):

    feedback: str = Field(
        description="Detailed feedback about the essay"
    )

    score: int = Field(
        description="Score out of 10",
        ge=0,
        le=10
    )


structured_model = model.with_structured_output(
    EvaluationSchema
)


# =========================
# ESSAY
# =========================

essay = """
Artificial Intelligence is changing the world rapidly.
It is being used in healthcare, education, agriculture,
business and many other fields.

India has a large number of engineers and technology
professionals, which gives it an opportunity to become
a major player in artificial intelligence.

AI can help farmers predict weather and improve crop
production. In healthcare, AI can help doctors detect
diseases. In education, AI can provide personalized
learning experiences.

However, AI also creates challenges. Automation may
replace some jobs, and there are concerns about privacy,
bias and misuse of data.

Therefore, India should focus on developing AI while
also ensuring that it is used responsibly and benefits
society.
"""


# =========================
# STATE
# =========================

class EssayState(TypedDict):

    essay: str

    language_feedback: str
    analysis_feedback: str
    clarity_feedback: str

    overall_feedback: str

    individual_scores: Annotated[
        list[int],
        operator.add
    ]

    avg_score: float


# =========================
# NODE 1
# LANGUAGE EVALUATION
# =========================

def evaluate_language(state: EssayState):

    prompt = f"""
    Evaluate the LANGUAGE QUALITY of the following essay.

    Consider:
    - Grammar
    - Vocabulary
    - Sentence structure
    - Word choice
    - Formality
    - Spelling

    Give detailed feedback and a score out of 10.

    Essay:
    {state["essay"]}
    """

    output = structured_model.invoke(prompt)

    return {
        "language_feedback": output.feedback,
        "individual_scores": [output.score]
    }


# =========================
# NODE 2
# ANALYSIS EVALUATION
# =========================

def evaluate_analysis(state: EssayState):

    prompt = f"""
    Evaluate the DEPTH OF ANALYSIS of the following essay.

    Consider:
    - Quality of arguments
    - Depth of explanation
    - Examples
    - Evidence
    - Critical thinking
    - Balance of different perspectives

    Give detailed feedback and a score out of 10.

    Essay:
    {state["essay"]}
    """

    output = structured_model.invoke(prompt)

    return {
        "analysis_feedback": output.feedback,
        "individual_scores": [output.score]
    }


# =========================
# NODE 3
# CLARITY EVALUATION
# =========================

def evaluate_clarity(state: EssayState):

    prompt = f"""
    Evaluate the CLARITY OF THOUGHT of the following essay.

    Consider:
    - Logical flow
    - Organization
    - Coherence
    - Transitions
    - Clear expression of ideas
    - Introduction and conclusion

    Give detailed feedback and a score out of 10.

    Essay:
    {state["essay"]}
    """

    output = structured_model.invoke(prompt)

    return {
        "clarity_feedback": output.feedback,
        "individual_scores": [output.score]
    }


# =========================
# FINAL EVALUATION
# =========================

def final_evaluation(state: EssayState):

    prompt = f"""
    Create a final summarized feedback for this essay.

    Language Feedback:
    {state["language_feedback"]}

    Analysis Feedback:
    {state["analysis_feedback"]}

    Clarity Feedback:
    {state["clarity_feedback"]}

    Give:
    1. Overall strengths
    2. Overall weaknesses
    3. Specific improvements
    """

    overall_feedback = model.invoke(prompt).content

    avg_score = (
        sum(state["individual_scores"])
        / len(state["individual_scores"])
    )

    return {
        "overall_feedback": overall_feedback,
        "avg_score": avg_score
    }


# =========================
# CREATE GRAPH
# =========================

graph = StateGraph(EssayState)


# Add nodes

graph.add_node(
    "evaluate_language",
    evaluate_language
)

graph.add_node(
    "evaluate_analysis",
    evaluate_analysis
)

graph.add_node(
    "evaluate_clarity",
    evaluate_clarity
)

graph.add_node(
    "final_evaluation",
    final_evaluation
)


# =========================
# PARALLEL EDGES
# =========================

graph.add_edge(
    START,
    "evaluate_language"
)

graph.add_edge(
    START,
    "evaluate_analysis"
)

graph.add_edge(
    START,
    "evaluate_clarity"
)


# =========================
# MERGE
# =========================

graph.add_edge(
    "evaluate_language",
    "final_evaluation"
)

graph.add_edge(
    "evaluate_analysis",
    "final_evaluation"
)

graph.add_edge(
    "evaluate_clarity",
    "final_evaluation"
)


# =========================
# END
# =========================

graph.add_edge(
    "final_evaluation",
    END
)


# =========================
# COMPILE
# =========================

workflow = graph.compile()


# =========================
# INITIAL STATE
# =========================

initial_state = {
    "essay": essay,

    "language_feedback": "",
    "analysis_feedback": "",
    "clarity_feedback": "",

    "overall_feedback": "",

    "individual_scores": [],

    "avg_score": 0.0
}


# =========================
# RUN
# =========================

result = workflow.invoke(initial_state)


# =========================
# OUTPUT
# =========================

print("\n==============================")
print("LANGUAGE FEEDBACK")
print("==============================")

print(result["language_feedback"])


print("\n==============================")
print("ANALYSIS FEEDBACK")
print("==============================")

print(result["analysis_feedback"])


print("\n==============================")
print("CLARITY FEEDBACK")
print("==============================")

print(result["clarity_feedback"])


print("\n==============================")
print("INDIVIDUAL SCORES")
print("==============================")

print(result["individual_scores"])


print("\n==============================")
print("AVERAGE SCORE")
print("==============================")

print(result["avg_score"])


print("\n==============================")
print("OVERALL FEEDBACK")
print("==============================")

print(result["overall_feedback"])