from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.state.state import AgentState
from src.tools.product_service.get_catalog import _get_catalog_impl
from src.model.model import llm
from src.utils.prompts import BASE_SYSTEM_PROMPT


class ProductAnswerResult(BaseModel):
    response_text: str = Field(
        description="La respuesta en lenguaje natural para el cliente, breve, "
        "solo con la información relevante a lo que preguntó."
    )
    product_resource_id: Optional[int] = Field(
        description="El id (tomado EXACTAMENTE de la lista [id: N] del catálogo "
        "que se te dio) del ÚNICO producto específico sobre el que giró la "
        "pregunta del cliente. Déjalo en null si la pregunta fue general "
        "(ej: '¿qué tienen?') o si mencionó varios productos distintos."
    )
    product_name: Optional[str] = Field(
        description="El nombre del producto identificado en product_resource_id, "
        "para uso interno. Null si product_resource_id es null."
    )

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

    structured_llm = llm.with_structured_output(ProductAnswerResult, method="function_calling")
    result = await structured_llm.ainvoke(messages)
    
    response = {"messages": [AIMessage(content=result.response_text)]}

    if result.product_resource_id is not None:
        response["last_product_discussed"] = {
            "resource_id": result.product_resource_id,
            "name": result.product_name,
        }

    return response