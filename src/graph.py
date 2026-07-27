from langgraph.graph import StateGraph, END
from src.state.state import AgentState
from src.nodes.intent import handled_intent
from src.nodes.bussines_information import business_information_node
from src.nodes.product_and_service_knowledge import product_service_knowledge_node
from src.nodes.handled_transaction import transaction_node
from src.nodes.human_assistance import human_assistance_node
from src.nodes.out_of_scope import out_of_scope_node
from src.router.router_by_intent import route_by_intent


def build_sales_agent_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("classify_intent", handled_intent)
    workflow.add_node("handle_business_info", business_information_node)
    workflow.add_node("handle_product_query", product_service_knowledge_node)
    workflow.add_node("handle_transaction", transaction_node)
    workflow.add_node("handle_human_request", human_assistance_node)
    workflow.add_node("handle_out_of_scope", out_of_scope_node)
    
    workflow.set_entry_point("classify_intent")
    
    workflow.add_conditional_edges(
        "classify_intent",
        route_by_intent
    )
    
    workflow.add_edge("handle_business_info", END)
    workflow.add_edge("handle_product_query", END)
    workflow.add_edge("handle_transaction", END)
    workflow.add_edge("handle_human_request", END)
    workflow.add_edge("handle_out_of_scope", END)
    
    return workflow.compile()


sales_agent = build_sales_agent_graph()