from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.graph import build_sales_agent_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.sales_agent = await build_sales_agent_graph()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {"status": "ok"}