from langchain_core.messages import HumanMessage, SystemMessage

from src.state.state import AgentState
from src.tools.bussines.get_bussines_information import _get_business_information_impl
from src.model.model import llm


async def greeting_node(state: AgentState) -> dict:
    """
    Responde cuando el cliente saluda o abre la conversación sin una pregunta
    específica todavía. No resuelve datos de pedido ni de catálogo -- solo da
    una bienvenida cálida y breve, mencionando el negocio, e invita al cliente
    a decir qué necesita.
    """
    business_info = await _get_business_information_impl(int(state["business_id"]))

    human_messages = [m for m in state["messages"] if isinstance(m, HumanMessage)]
    last_message = human_messages[-1] if human_messages else None

    system_prompt = (
        "Eres el asistente de atención al cliente de este negocio. El cliente "
        "acaba de saludar o abrir la conversación, sin una pregunta específica "
        "todavía. Responde con un saludo cálido y breve, menciona el nombre "
        "del negocio de forma natural, e invita al cliente a contarte qué "
        "necesita (productos, horarios, hacer un pedido, etc.). NO enumeres "
        "el catálogo ni todos los datos del negocio -- es solo una bienvenida. "
        "Responde en el mismo idioma en que escribió el cliente.\n\n"
        f"Información del negocio:\n{business_info}"
    )

    messages = [SystemMessage(content=system_prompt)]
    if last_message:
        messages.append(last_message)

    response = await llm.ainvoke(messages)

    return {"messages": [response]}
