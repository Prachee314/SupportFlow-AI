from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from src.state import SupportState
from src.agents import (
    triage_node,
    priority_node,
    database_node,
    resolution_node,
    execute_action_node
)

workflow = StateGraph(SupportState)

# Nodes
workflow.add_node("triage", triage_node)
workflow.add_node("priority", priority_node)
workflow.add_node("database", database_node)
workflow.add_node("resolution", resolution_node)
workflow.add_node("human_review", lambda state: state)
workflow.add_node("execute_action", execute_action_node)

# Entry
workflow.set_entry_point("triage")

# Flow
workflow.add_edge("triage", "priority")
workflow.add_edge("priority", "database")
workflow.add_edge("database", "resolution")
workflow.add_edge("resolution", "human_review")


# Human Review Routing
def route_after_review(state: SupportState):
    if state.get("supervisor_approved") is True:
        return "execute_action"

    return "resolution"


workflow.add_conditional_edges(
    "human_review",
    route_after_review
)

workflow.add_edge("execute_action", END)

# Memory + HITL
memory = MemorySaver()

app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["human_review"]
)