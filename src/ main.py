from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from src.graph import build_sales_agent_graph
from app.database import async_session_maker
from app.repositories.conversation_repository import get_or_create_conversation
from app.models_conversation import Channel


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.sales_agent = await build_sales_agent_graph()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok"}


class MessageRequest(BaseModel):
    message: str
    business_id: int
    phone_number: str


@app.post("/chat")
async def chat(request: MessageRequest):
    async with async_session_maker() as session:
        conversation = await get_or_create_conversation(
            session,
            business_id=request.business_id,
            external_user_id=request.phone_number,
            channel=Channel.WHATSAPP,
        )
        await session.commit()

    thread_id = str(conversation.id)
    config = {"configurable": {"thread_id": thread_id}}

    result = await app.state.sales_agent.ainvoke(
        {
            "messages": [HumanMessage(content=request.message)],
            "business_id": request.business_id,
        },
        config=config,
    )

    return {
        "response": result["messages"][-1].content,
        "intent": result["intent"],
        "conversation_id": conversation.id,  # útil para verificar en tus pruebas
    }