from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.router import router_agent
from agents.coding_agent import coding_agent
from agents.documentation_agent import documentation_agent
from agents.rag_agent import rag_agent
from agents.reflection_agent import reflection_agent


# -----------------------------
# Graph State
# -----------------------------
class AgentState(TypedDict):

    question:str

    agent:str

    answer:str

    sources:list


# -----------------------------
# Router Node
# -----------------------------
def router_node(state: AgentState):

    question = state["question"]

    selected_agent = router_agent(question)

    state["agent"] = selected_agent

    return state


# -----------------------------
# Coding Agent Node
# -----------------------------
def coding_node(state: AgentState):

    answer = coding_agent(state["question"])

    state["answer"] = answer

    state["sources"] = []

    return state

# -----------------------------
# Documentation Agent Node
# -----------------------------
def documentation_node(state: AgentState):

    answer = documentation_agent(state["question"])

    state["answer"] = answer

    state["sources"] = []

    return state


# -----------------------------
# RAG Agent Node
# -----------------------------
def rag_node(state: AgentState):

    result = rag_agent(state["question"])

    state["answer"] = result["answer"]

    state["sources"] = result["sources"]

    return state

# -----------------------------
# Reflection Node
# -----------------------------
def reflection_node(state: AgentState):

    improved_answer = reflection_agent(state["answer"])

    state["answer"] = improved_answer

    return state


# -----------------------------
# Conditional Routing
# -----------------------------
def route(state: AgentState):

    return state["agent"]


# -----------------------------
# Build Graph
# -----------------------------
builder = StateGraph(AgentState)

builder.add_node("router", router_node)
builder.add_node("coding", coding_node)
builder.add_node("documentation", documentation_node)
builder.add_node("rag", rag_node)
builder.add_node("reflection", reflection_node)


# -----------------------------
# Entry Point
# -----------------------------
builder.set_entry_point("router")


# -----------------------------
# Router → Agents
# -----------------------------
builder.add_conditional_edges(
    "router",
    route,
    {
        "coding": "coding",
        "documentation": "documentation",
        "rag": "rag"
    }
)


# -----------------------------
# Agents → Reflection
# -----------------------------
builder.add_edge("coding", "reflection")
builder.add_edge("documentation", "reflection")
builder.add_edge("rag", "reflection")


# -----------------------------
# Reflection → End
# -----------------------------
builder.add_edge("reflection", END)


# -----------------------------
# Compile Graph
# -----------------------------
graph = builder.compile()