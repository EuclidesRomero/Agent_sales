from langchain_core.tools import tool
from src.app.database import async_session_maker
from src.app.repositories.catalog_repository import search_catalog


async def _get_catalog_impl(business_id: int) -> str:
    """
    Implementación interna para obtener el catálogo de productos y servicios.
    """
    async with async_session_maker() as db:
        catalog = await search_catalog(db, business_id)
        catalog_text = ""
        for resource in catalog:
            catalog_text += f"\n[id: {resource.id}] {resource.name} ({resource.type.value})"
            if resource.description:
                catalog_text += f": {resource.description}"
            if resource.variants:
                catalog_text += "\n  Variantes:"
                for variant in resource.variants:
                    catalog_text += f"\n  - {variant.name}: ${variant.price}"
                    if variant.stock is not None:
                        catalog_text += f" (Stock: {variant.stock})"
        
        return catalog_text if catalog_text else "No hay productos/servicios disponibles"


@tool
async def get_catalog(business_id: int) -> str:
    """
    Devuelve el catálogo completo de productos y servicios de un negocio: nombres,
    tipos, descripciones, variantes, precios y stock disponible.

    Úsala cuando el cliente pregunte por productos, servicios, precios, disponibilidad,
    o cualquier pregunta específica sobre el catálogo del negocio (para información
    general del negocio como ubicación o horarios, usa get_business_information).

    Args:
        business_id: id del negocio que está siendo atendido en la conversación actual.
    """
    return await _get_catalog_impl(business_id)
