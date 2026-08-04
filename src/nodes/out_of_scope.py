from src.state.state import AgentState
from langchain_core.messages import AIMessage


async def out_of_scope_node(state: AgentState) -> AgentState:
    response = "I'm sorry, but I can only help with questions about our business, products, services, and purchases. For other topics, I'm unable to assist you. Is there anything else I can help you with regarding our business?"
    
    state["messages"].append(AIMessage(content=response))
    
    return state
