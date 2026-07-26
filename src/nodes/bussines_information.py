from src.state.state import AgentState
from src.tools.bussines.get_bussines_information import get_business_information

async def business_information_node(state: AgentState) -> AgentState:
    business_info = await get_business_information(int(state["business_id"]))
    return {**state, "business_info": {"information": business_info}}
