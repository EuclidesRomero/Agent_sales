import json
from state.state import AgentState
from model.model import llm
from langchain_core.messages import HumanMessage, SystemMessage


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
- unknown: The intent is unclear or doesn't fit any category

Respond with only the intent name and a confidence score between 0 and 1, in JSON format: {"name": "intent", "confidence": 0.95}"""
    
    last_message = state["messages"][-1] if state["messages"] else None
    
    if last_message:
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=last_message.content)
        ])
        
        intent_result = json.loads(response.content)
        state["intent"]["name"] = intent_result["name"]
        state["intent"]["confidence"] = intent_result["confidence"]
    
    return state
