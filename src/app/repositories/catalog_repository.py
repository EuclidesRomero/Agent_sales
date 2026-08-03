from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from src.app.models import BusinessResource, ResourceType


async def search_catalog(
    db: AsyncSession,
    business_id: int,
    search_query: str | None = None,
    resource_type: ResourceType | None = None,
    category_id: int | None = None,
    active_only: bool = True,
) -> list[BusinessResource]:
    """
    Search business resources (products/services) with optional filters.
    Returns resources with their variants preloaded.
    """
    query = (
        select(BusinessResource)
        .options(selectinload(BusinessResource.variants))
        .where(BusinessResource.business_id == business_id)
    )

    if active_only:
        query = query.where(BusinessResource.active == True)

    if resource_type:
        query = query.where(BusinessResource.type == resource_type)

    if category_id:
        query = query.where(BusinessResource.category_id == category_id)

    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.where(
            or_(
                BusinessResource.name.ilike(search_pattern),
                BusinessResource.description.ilike(search_pattern),
            )
        )

    result = await db.execute(query)
    return list(result.scalars().all())
