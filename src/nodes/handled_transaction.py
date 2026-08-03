from src.state.state import AgentState
from langchain_core.messages import AIMessage


async def transaction_node(state: AgentState) -> AgentState:
    response = "I'd be happy to help you with your purchase. However, the transaction processing system is still being configured. For now, please contact our business directly to complete your purchase or reach out to a human agent for assistance."
    
    state["messages"].append(AIMessage(content=response))
    
    return state