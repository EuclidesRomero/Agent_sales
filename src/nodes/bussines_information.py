from state.state import AgentState
from model.model import llm
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from tools.bussines.get_bussines_information import get_bussines_information


def handle_business_info(state: AgentState) -> AgentState:
    last_message = state["messages"][-1] if state["messages"] else None
    
    if last_message:
        business_info = get_bussines_information(
            business_id=state["business_id"],
            query=last_message.content
        )
        
        system_prompt = """You are a helpful business assistant. Use the provided business information to answer the user's question naturally and helpfully."""
        
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User question: {last_message.content}\n\nBusiness information: {business_info}")
        ])
        
        state["business_info"]["information"] = {
            "query": last_message.content,
            "response": response.content,
            "raw_data": business_info
        }
        
        state["messages"].append(AIMessage(content=response.content))
    
    return state
