from langchain_core.tools import tool
from app.database import async_session_maker
from app.repositories.business_repository import build_business_context

@tool
async def get_business_information(business_id: int) -> dict:
    """
    Devuelve la información general de un negocio: datos de contacto, ubicación,
    horarios de atención y preguntas frecuentes (FAQ) registradas.

    Úsala cuando el cliente pregunte por ubicación, teléfono, si hacen domicilios,
    horarios de atención, o cualquier pregunta general sobre el negocio que NO sea
    sobre un producto o servicio específico del catálogo (para eso existe
    search_catalog / get_product_details, no esta tool).

    Args:
        business_id: id del negocio que está siendo atendido en la conversación actual.
    """
    async with async_session_maker() as session:
        return await build_business_context(session, business_id)