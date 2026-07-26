from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.router import router_agent
from agents.coding_agent import coding_agent
from agents.documentation_agent import documentation_agent
from agents.rag_agent import rag_agent
from agents.reflection_agent import reflection_agent

from agents.testing_agent import testing_agent
from agents.architecture_agent import architecture_agent
from agents.code_review_agent import code_review_agent
from agents.upload_rag_agent import upload_rag_agent


class AgentState(TypedDict):

    question: str

    agent: str

    answer: str

    sources: list


def router_node(state: AgentState):

    question = state["question"]

    selected_agent = router_agent(question)

    state["agent"] = selected_agent

    return state



def coding_node(state: AgentState):

    answer = coding_agent(
        state["question"]
    )

    state["answer"] = answer

    state["sources"] = []

    return state



def documentation_node(state: AgentState):

    answer = documentation_agent(
        state["question"]
    )

    state["answer"] = answer

    state["sources"] = []

    return state


def rag_node(state: AgentState):

    result = rag_agent(
        state["question"]
    )


    state["answer"] = result["answer"]

    state["sources"] = result["sources"]

    return state


def testing_node(state: AgentState):

    answer = testing_agent(
        state["question"]
    )


    state["answer"] = answer

    state["sources"] = []

    return state


def architecture_node(state: AgentState):

    answer = architecture_agent(
        state["question"]
    )


    state["answer"] = answer

    state["sources"] = []

    return state


def code_review_node(state: AgentState):

    answer = code_review_agent(
        state["question"]
    )


    state["answer"] = answer

    state["sources"] = []

    return state


def reflection_node(state: AgentState):

    improved_answer = reflection_agent(
        state["answer"]
    )


    state["answer"] = improved_answer

    return state


def upload_rag_node(state):

    result = upload_rag_agent(

        state["question"]

    )

    state["answer"] = result["answer"]

    state["sources"] = result["sources"]

    return state


def route(state: AgentState):

    return state["agent"]


builder = StateGraph(AgentState)


builder.add_node(
    "router",
    router_node
)


builder.add_node(
    "coding",
    coding_node
)


builder.add_node(
    "documentation",
    documentation_node
)


builder.add_node(
    "rag",
    rag_node
)


builder.add_node(
    "testing",
    testing_node
)


builder.add_node(
    "architecture",
    architecture_node
)


builder.add_node(
    "code_review",
    code_review_node
)


builder.add_node(
    "reflection",
    reflection_node
)

builder.add_node(

    "upload_rag",

    upload_rag_node

)



builder.set_entry_point(
    "router"
)


builder.add_conditional_edges(

    "router",

    route,

    {        "coding": "coding",

        "documentation": "documentation",

        "rag": "rag",

        "testing": "testing",

        "architecture": "architecture",

        "code_review": "code_review",
        "upload_rag":"upload_rag",

    }

)




builder.add_edge(
    "coding",
    "reflection"
)


builder.add_edge(
    "documentation",
    "reflection"
)


builder.add_edge(
    "rag",
    "reflection"
)


builder.add_edge(
    "testing",
    "reflection"
)


builder.add_edge(
    "architecture",
    "reflection"
)


builder.add_edge(
    "code_review",
    "reflection"
)



builder.add_edge(
    "reflection",
    END
)

builder.add_edge(

    "upload_rag",

    "reflection"

)



graph = builder.compile()