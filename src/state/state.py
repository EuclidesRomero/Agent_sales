from typing import Annotated, Sequence, Literal, Optional
from typing_extensions import TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages




class IntentState(TypedDict):
    name: Optional[Literal[
        "business_information",
        "product_service_knowledge",
        "transaction",
        "human_request",
        "out_of_scope",
        "unknown",
    ]]
    confidence: Optional[float]


class CustomerState(TypedDict):
    name: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    payment_method: Optional[str]


class ProductQueryState(TypedDict):
    query: Optional[str]
    results: list[dict]
    selected_product: Optional[dict]


class BusinessInfoState(TypedDict):
    information: Optional[dict]


class OrderItem(TypedDict):
    product_name: str
    quantity: int


class TransactionState(TypedDict):
    items: list[OrderItem]
    is_complete: bool
    requires_human: bool
    request_id: Optional[str]




class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    business_id: str
    intent: IntentState
    customer: CustomerState
    product_query: ProductQueryState
    business_info: BusinessInfoState
    transaction: TransactionState