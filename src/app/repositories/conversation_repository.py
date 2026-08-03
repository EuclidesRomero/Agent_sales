from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models_conversation import Conversation, ConversationStatus, Channel


async def get_or_create_conversation(
    session: AsyncSession,
    business_id: int,
    external_user_id: str,
    channel: Channel,
) -> Conversation:
    """
    Busca una conversación ACTIVA para este negocio y este cliente.
    Si no existe, crea una nueva.
    """
    result = await session.execute(
        select(Conversation).where(
            Conversation.business_id == business_id,
            Conversation.external_user_id == external_user_id,
            Conversation.status == ConversationStatus.ACTIVE,
        )
    )
    conversation = result.scalar_one_or_none()

    if conversation:
        return conversation

    new_conversation = Conversation(
        business_id=business_id,
        external_user_id=external_user_id,
        channel=channel,
        status=ConversationStatus.ACTIVE,
    )
    session.add(new_conversation)
    await session.flush()
    return new_conversation