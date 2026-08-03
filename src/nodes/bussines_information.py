from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.state.state import AgentState
from src.tools.bussines.get_bussines_information import _get_business_information_impl
from src.model.model import llm
from src.utils.prompts import BASE_SYSTEM_PROMPT


async def business_information_node(state: AgentState) -> dict:
    business_info = await _get_business_information_impl(int(state["business_id"]))
    human_messages = [m for m in state["messages"] if isinstance(m, HumanMessage)]
    last_message = human_messages[-1] if human_messages else None

    system_prompt = (
        BASE_SYSTEM_PROMPT +
        f"Información completa del negocio (usa solo lo relevante):\n{business_info}"
    )

    messages = [SystemMessage(content=system_prompt)]
    if last_message:
        messages.append(last_message)

    response = await llm.ainvoke(messages)

    return {
        "messages": [response],
        "business_info": {"information": business_info},
    }