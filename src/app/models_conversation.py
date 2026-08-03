from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Enum as SqlEnum,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.database import Base
from src.app.models import TimestampMixin


class Channel(str, Enum):
    WHATSAPP = "WHATSAPP"
    TELEGRAM = "TELEGRAM"
    WEB = "WEB"
    INSTAGRAM = "INSTAGRAM"
    OTHER = "OTHER"


class ConversationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    TRANSFERRED = "TRANSFERRED"


class MessageRole(str, Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    SYSTEM = "SYSTEM"
    TOOL = "TOOL"


class LeadStatus(str, Enum):
    NEW = "NEW"
    QUALIFIED = "QUALIFIED"
    CONTACTED = "CONTACTED"
    CLOSED = "CLOSED"


class Conversation(Base, TimestampMixin):
    __tablename__ = "conversations"

    __table_args__ = (
        Index(
            "ix_conversations_business_status",
            "business_id",
            "status",
        ),
        Index(
            "ux_conversations_one_active_per_customer",
            "business_id",
            "external_user_id",
            unique=True,
            postgresql_where=text("status = 'ACTIVE'"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    business_id: Mapped[int] = mapped_column(
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    external_user_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    channel: Mapped[Channel] = mapped_column(SqlEnum(Channel), nullable=False)

    status: Mapped[ConversationStatus] = mapped_column(
        SqlEnum(ConversationStatus),
        default=ConversationStatus.ACTIVE,
        nullable=False,
    )

    business: Mapped["Business"] = relationship()

    messages: Mapped[list["Message"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )

    leads: Mapped[list["Lead"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
    )

    intents: Mapped[list["ConversationIntent"]] = relationship(
        back_populates="conversation",
        cascade="all, delete-orphan",
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    role: Mapped[MessageRole] = mapped_column(SqlEnum(MessageRole), nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    tool_payload: Mapped[dict | None] = mapped_column(JSONB)

    extra_metadata: Mapped[dict | None] = mapped_column(JSONB)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")


class Lead(Base, TimestampMixin):
    __tablename__ = "leads"

    __table_args__ = (
        Index(
            "ix_leads_business_status",
            "business_id",
            "status",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    business_id: Mapped[int] = mapped_column(
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    resource_id: Mapped[int | None] = mapped_column(
        ForeignKey("business_resources.id", ondelete="SET NULL"),
        index=True,
    )

    customer_name: Mapped[str | None] = mapped_column(String(150))

    customer_phone: Mapped[str | None] = mapped_column(String(30))

    interest: Mapped[str] = mapped_column(Text, nullable=False)

    details: Mapped[dict | None] = mapped_column(JSONB)

    status: Mapped[LeadStatus] = mapped_column(
        SqlEnum(LeadStatus),
        default=LeadStatus.NEW,
        nullable=False,
    )

    contacted_at: Mapped[datetime | None]

    business: Mapped["Business"] = relationship(back_populates="leads", passive_deletes=True)

    conversation: Mapped["Conversation"] = relationship(back_populates="leads")

    resource: Mapped["BusinessResource | None"] = relationship(back_populates="leads", passive_deletes=True)


class ConversationIntent(Base):
    __tablename__ = "conversation_intents"

    __table_args__ = (
        CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="ck_confidence_range",
        ),
        Index(
            "ux_conversation_intents_one_current",
            "conversation_id",
            unique=True,
            postgresql_where=text("is_current = true"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    message_id: Mapped[int | None] = mapped_column(
        ForeignKey("messages.id", ondelete="SET NULL"),
        index=True,
    )

    intent: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    confidence: Mapped[Decimal | None] = mapped_column(Numeric(4, 3))

    is_current: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    raw_payload: Mapped[dict | None] = mapped_column(JSONB)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    conversation: Mapped["Conversation"] = relationship(back_populates="intents")

    message: Mapped["Message | None"] = relationship()