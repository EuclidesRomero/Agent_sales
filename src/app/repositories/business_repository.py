from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models import Business, KnowledgeDocument, DocumentType


async def build_business_context(session: AsyncSession, business_id: int) -> dict | None:
    result = await session.execute(
        select(Business)
        .options(selectinload(Business.hours))
        .where(Business.id == business_id)
    )
    business = result.scalar_one_or_none()
    if business is None:
        return None

    faqs_result = await session.execute(
        select(KnowledgeDocument).where(
            KnowledgeDocument.business_id == business_id,
            KnowledgeDocument.document_type == DocumentType.FAQ,
        )
    )
    faqs_docs = faqs_result.scalars().all()

    hours = [
        {
            "day_of_week": h.day_of_week,
            "open_time": h.open_time.strftime("%H:%M:%S") if h.open_time else None,
            "close_time": h.close_time.strftime("%H:%M:%S") if h.close_time else None,
            "is_closed": h.is_closed,
        }
        for h in business.hours
    ]
    faqs = [{"question": f.title, "answer": f.content} for f in faqs_docs]

    return {
        "name": business.name,
        "description": business.description,
        "phone": business.phone,
        "email": business.email,
        "website": business.website,
        "address": business.address,
        "city": business.city,
        "country": business.country,
        "hours": hours,
        "faqs": faqs,
    }