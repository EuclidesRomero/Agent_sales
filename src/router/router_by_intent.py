from state.state import AgentState

def route_by_intent(state: AgentState) -> str:
    intent_name = state["intent"]["name"]

    intent_to_node = {
        "business_information": "handle_business_info",
        "product_service_knowledge": "handle_product_query",
        "transaction": "handle_transaction",
        "human_request": "handle_human_request",
        "unknown": "handle_out_of_scope",
        "out_of_scope": "handle_out_of_scope",
    }

    return intent_to_node.get(
        intent_name,
        "handle_out_of_scope"
    )
