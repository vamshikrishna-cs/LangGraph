from langgraph.types import interrupt



def human_review_node(state):
    reviewed = interrupt(state)
    return reviewed

