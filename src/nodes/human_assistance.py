from src.state.state import AgentState
from langchain_core.messages import AIMessage


async def human_assistance_node(state: AgentState) -> AgentState:
    response = "I understand you'd like to speak with a human agent. Let me connect you with our team. A human representative will be with you shortly to assist you with your request."
    
    state["messages"].append(AIMessage(content=response))
    
    return state