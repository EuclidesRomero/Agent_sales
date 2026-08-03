from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.state.state import AgentState
from src.tools.product_service.get_catalog import _get_catalog_impl
from src.model.model import llm
from src.utils.prompts import BASE_SYSTEM_PROMPT


async def product_service_knowledge_node(state: AgentState) -> dict:
    catalog = await _get_catalog_impl(int(state["business_id"]))
    human_messages = [m for m in state["messages"] if isinstance(m, HumanMessage)]
    last_message = human_messages[-1] if human_messages else None

    system_prompt = (
        BASE_SYSTEM_PROMPT +
        f"Catálogo de productos y servicios (usa solo lo relevante):\n{catalog}"
    )

    messages = [SystemMessage(content=system_prompt)]
    if last_message:
        messages.append(last_message)

    response = await llm.ainvoke(messages)

    return {
        "messages": [response],
        "catalog_info": {"information": catalog},
    }
