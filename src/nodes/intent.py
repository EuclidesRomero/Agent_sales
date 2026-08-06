from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage

from src.state.state import AgentState
from src.model.model import llm


class IntentResult(BaseModel):
    name: str = Field(description="The classified intent name")
    confidence: float = Field(description="Confidence score between 0 and 1")


SYSTEM_PROMPT = """You are an intent classifier for a business sales assistant. Respond in JSON format.

The agent only handles:
- Business information
- Products or services
- Purchase requests
- Human assistance

If the user asks about unrelated topics, classify as out_of_scope.

Never classify unrelated questions as business_information or product_service_knowledge.

Classify the user's intent into one of the following categories:
- business_information: User is asking for information about the business (hours, location, contact, etc.)
- product_service_knowledge: User is asking about products or services offered
- transaction: User wants to make a purchase or complete a transaction
- human_request: User explicitly requests to speak with a human agent
- out_of_scope: User asks about topics unrelated to the business, products, or services
- unknown: The intent is unclear or doesn't fit any category

Your response must be a valid JSON object with 'name' and 'confidence' fields."""


async def handled_intent(state: AgentState) -> dict:
    human_messages = [m for m in state["messages"] if isinstance(m, HumanMessage)]
    last_message = human_messages[-1] if human_messages else None

    if last_message is None:
        return {"intent": {"name": "unknown", "confidence": 0.0}}

    structured_llm = llm.with_structured_output(IntentResult, method="function_calling")
    response = await structured_llm.ainvoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=last_message.content),
    ])

    # Devolvemos SOLO lo que cambió, no el estado completo mutado --
    # así LangGraph aplica el merge correctamente sobre el resto del state.
    return {"intent": {"name": response.name, "confidence": response.confidence}}