CONFIDENCE_THRESHOLD = 0.7


def confidence_router(state):

    if state.get("human_approved"):
        return "planner"

    if state["overall_confidence"] < CONFIDENCE_THRESHOLD:
        return "review"

    return "planner"
