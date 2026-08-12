from datetime import datetime, timedelta, timezone
from typing import NamedTuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models_conversation import Conversation, ConversationStatus, Channel

CONVERSATION_TIMEOUT = timedelta(minutes=2)


class ConversationResult(NamedTuple):
    conversation: Conversation
    stale_conversation_id: int | None  


async def get_or_create_conversation(
    session: AsyncSession,
    business_id: int,
    external_user_id: str,
    channel: Channel,
) -> ConversationResult:
    """
    Busca una conversación ACTIVA para este negocio y este cliente.

    - Si existe y está vigente (menos de CONVERSATION_TIMEOUT desde el último
      mensaje), la reutiliza y refresca su updated_at.
    - Si existe pero quedó vieja (más de CONVERSATION_TIMEOUT sin actividad),
      la cierra (status=CLOSED) y crea una nueva -- devuelve el id de la vieja
      para que quien llame a esta función pueda borrar su thread del
      checkpointer de LangGraph.
    - Si no existe ninguna, crea una nueva.
    """
    result = await session.execute(
        select(Conversation).where(
            Conversation.business_id == business_id,
            Conversation.external_user_id == external_user_id,
            Conversation.status == ConversationStatus.ACTIVE,
        )
    )
    conversation = result.scalar_one_or_none()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if conversation:
        is_stale = (now - conversation.updated_at) > CONVERSATION_TIMEOUT

        if is_stale:
            stale_id = conversation.id
            conversation.status = ConversationStatus.CLOSED
            await session.flush()

            new_conversation = Conversation(
                business_id=business_id,
                external_user_id=external_user_id,
                channel=channel,
                status=ConversationStatus.ACTIVE,
            )
            session.add(new_conversation)
            await session.flush()
            return ConversationResult(conversation=new_conversation, stale_conversation_id=stale_id)

        conversation.updated_at = now
        await session.flush()
        return ConversationResult(conversation=conversation, stale_conversation_id=None)

    new_conversation = Conversation(
        business_id=business_id,
        external_user_id=external_user_id,
        channel=channel,
        status=ConversationStatus.ACTIVE,
    )
    session.add(new_conversation)
    await session.flush()
    return ConversationResult(conversation=new_conversation, stale_conversation_id=None)