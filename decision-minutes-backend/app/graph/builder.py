from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.graph.state import GraphState
from app.graph.nodes.asr import asr_node
from app.graph.nodes.extract import extract_node
from app.graph.nodes.confidence import confidence_router
from app.graph.nodes.review import human_review_node
from app.graph.nodes.planner import planner_node


def build_graph():

    builder = StateGraph(GraphState)

    builder.add_node("asr", asr_node)
    builder.add_node("extract", extract_node)
    builder.add_node("review", human_review_node)
    builder.add_node("planner", planner_node)

    builder.set_entry_point("asr")

    builder.add_edge("asr", "extract")

    builder.add_conditional_edges(
        "extract",
        confidence_router,
        {
            "review": "review",
            "planner": "planner"
        }
    )

    builder.add_edge("review", "planner")
    builder.add_edge("planner", END)

    memory = MemorySaver()

    return builder.compile(checkpointer=memory)
