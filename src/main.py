from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from src.graph import build_sales_agent_graph, close_pool
from src.app.database import async_session_maker
from src.app.repositories.conversation_repository import get_or_create_conversation
from src.app.models_conversation import Channel


@asynccontextmanager
async def lifespan(app: FastAPI):
    graph, checkpointer = await build_sales_agent_graph()
    app.state.sales_agent = graph
    app.state.checkpointer = checkpointer
    yield
    await close_pool()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        result = await get_or_create_conversation(
            session,
            business_id=request.business_id,
            external_user_id=request.phone_number,
            channel=Channel.WHATSAPP,
        )
        await session.commit()

    if result.stale_conversation_id is not None:
        await app.state.checkpointer.adelete_thread(str(result.stale_conversation_id))

    thread_id = str(result.conversation.id)
    config = {"configurable": {"thread_id": thread_id}}

    agent_result = await app.state.sales_agent.ainvoke(
        {"messages": [HumanMessage(content=request.message)], "business_id": request.business_id},
        config=config,
    )

    return {
        "response": agent_result["messages"][-1].content,
        "intent": agent_result["intent"],
        "conversation_id": result.conversation.id,
        "last_product_discussed": agent_result.get("last_product_discussed"),
    }