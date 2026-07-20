from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):
    cv_text: str
    candidate_profile: Dict[str, Any]
    job_offers: List[Dict[str, Any]]
    analyzed_offers: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]



