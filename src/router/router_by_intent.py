from langchain_core.messages import HumanMessage
from src.helpers.soudns_like_confirmation import _sounds_like_confirmation

from src.state.state import AgentState


async def route_entry(state: AgentState) -> str:
    transaction = state.get("transaction")
    if transaction and transaction.get("items") and not transaction.get("is_complete"):
        return "handle_transaction"

    product_query = state.get("product_query")
    if product_query and product_query.get("results"):
        return "handle_transaction"

    last_product = state.get("last_product_discussed")
    if last_product:
        human_messages = [m for m in state["messages"] if isinstance(m, HumanMessage)]
        last_message = human_messages[-1] if human_messages else None
        if last_message and _sounds_like_confirmation(last_message.content):
            return "handle_transaction"

    return "classify_intent"


async def route_by_intent(state: AgentState) -> str:
    intent_name = state["intent"]["name"]

    intent_to_node = {
        "greeting": "handle_greeting",
        "business_information": "handle_business_info",
        "product_service_knowledge": "handle_product_query",
        "transaction": "handle_transaction",
        "human_request": "handle_human_request",
        "unknown": "handle_out_of_scope",
        "out_of_scope": "handle_out_of_scope",
    }

    return intent_to_node.get(intent_name, "handle_out_of_scope")