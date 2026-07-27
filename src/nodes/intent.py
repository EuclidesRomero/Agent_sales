from pydantic import BaseModel, Field
from src.state.state import AgentState
from src.model.model import llm
from langchain_core.messages import HumanMessage, SystemMessage


class IntentResult(BaseModel):
    name: str = Field(description="The classified intent name")
    confidence: float = Field(description="Confidence score between 0 and 1")


def handled_intent(state: AgentState) -> AgentState:
    system_prompt = """You are an intent classifier for a business sales assistant.

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
- unknown: The intent is unclear or doesn't fit any category"""
    
    last_message = state["messages"][-1] if state["messages"] else None
    
    if last_message:
        structured_llm = llm.with_structured_output(IntentResult)
        response = structured_llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=last_message.content)
        ])
        
        state["intent"]["name"] = response.name
        state["intent"]["confidence"] = response.confidence
    
    return state
