from langgraph.graph import StateGraph, END
from backend.schema import GraphState
from backend.nodes import analyzer_node, general_node, policy_node

def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("analyzer", analyzer_node)
    graph.add_node("general", general_node)
    graph.add_node("policy", policy_node)

    graph.set_entry_point("analyzer")

    graph.add_conditional_edges(
        "analyzer",
        lambda state: state["route"],
        {
            "general": "general",
            "policy": "policy"
        }
    )

    graph.add_edge("general", END)
    graph.add_edge("policy", END)

    return graph.compile()