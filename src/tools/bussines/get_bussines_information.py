from typing import Optional
from langchain_core.tools import tool


@tool
def get_bussines_information(business_id: str, query: str) -> dict:
    """
    Retrieve business information based on the business ID and user query.
    
    Args:
        business_id: The unique identifier for the business
        query: The specific information being requested (e.g., "hours", "location", "contact")
    
    Returns:
        A dictionary containing the requested business information
    """
    business_data = {
        "hours": "Monday-Friday: 9AM-6PM, Saturday: 10AM-4PM, Sunday: Closed",
        "location": "123 Main Street, City, State 12345",
        "contact": {
            "phone": "+1 (555) 123-4567",
            "email": "contact@business.com"
        },
        "services": ["Product sales", "Consultations", "Support", "Custom orders"],
        "policies": {
            "returns": "30-day return policy with original receipt",
            "warranty": "1-year warranty on all products"
        }
    }
    
    query_lower = query.lower()
    
    if "hour" in query_lower:
        return {"hours": business_data["hours"]}
    elif "location" in query_lower or "address" in query_lower:
        return {"location": business_data["location"]}
    elif "contact" in query_lower or "phone" in query_lower or "email" in query_lower:
        return {"contact": business_data["contact"]}
    elif "service" in query_lower:
        return {"services": business_data["services"]}
    elif "policy" in query_lower or "return" in query_lower or "warranty" in query_lower:
        return {"policies": business_data["policies"]}
    else:
        return {"all_info": business_data}
