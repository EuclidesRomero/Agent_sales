
from datetime import datetime, time
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Boolean,
    Enum as SqlEnum,
    ForeignKey,
    Numeric,
    String,
    Text,
    Time,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.database import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class ResourceType(str, Enum):
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    PLAN = "PLAN"
    PACKAGE = "PACKAGE"
    PROMOTION = "PROMOTION"


class DocumentType(str, Enum):
    FAQ = "FAQ"
    POLICY = "POLICY"
    BUSINESS_INFO = "BUSINESS_INFO"
    TONE_INSTRUCTIONS = "TONE_INSTRUCTIONS"
    PRODUCT_INFO = "PRODUCT_INFO"
    OTHER = "OTHER"


class Business(Base, TimestampMixin):
    __tablename__ = "businesses"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(150), nullable=False)

    description: Mapped[str | None] = mapped_column(Text)

    phone: Mapped[str | None] = mapped_column(String(30))

    email: Mapped[str | None] = mapped_column(String(150))

    website: Mapped[str | None] = mapped_column(String(255))

    address: Mapped[str | None] = mapped_column(String(255))

    city: Mapped[str | None] = mapped_column(String(100))

    country: Mapped[str | None] = mapped_column(String(100))

    resources: Mapped[list["BusinessResource"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )

    categories: Mapped[list["Category"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )

    hours: Mapped[list["BusinessHour"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )

    knowledge_documents: Mapped[list["KnowledgeDocument"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )

    leads: Mapped[list["Lead"]] = relationship(
        back_populates="business",
        passive_deletes=True,
    )


class BusinessHour(Base, TimestampMixin):
    __tablename__ = "business_hours"
    __table_args__ = (
        UniqueConstraint("business_id", "day_of_week", name="uq_business_day"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    business_id: Mapped[int] = mapped_column(
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    day_of_week: Mapped[int] = mapped_column(nullable=False)

    open_time: Mapped[time | None] = mapped_column(Time)

    close_time: Mapped[time | None] = mapped_column(Time)

    is_closed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    business: Mapped["Business"] = relationship(back_populates="hours")


class Category(Base, TimestampMixin):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)

    business_id: Mapped[int] = mapped_column(
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        index=True,
    )

    business: Mapped["Business"] = relationship(back_populates="categories")

    parent: Mapped["Category | None"] = relationship(
        remote_side="Category.id",
        back_populates="children",
    )

    children: Mapped[list["Category"]] = relationship(
        back_populates="parent",
    )

    resources: Mapped[list["BusinessResource"]] = relationship(
        back_populates="category",
    )


class BusinessResource(Base, TimestampMixin):
    __tablename__ = "business_resources"

    id: Mapped[int] = mapped_column(primary_key=True)

    business_id: Mapped[int] = mapped_column(
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        index=True,
    )

    type: Mapped[ResourceType] = mapped_column(SqlEnum(ResourceType), nullable=False)

    name: Mapped[str] = mapped_column(String(150), nullable=False)

    description: Mapped[str | None] = mapped_column(Text)

    attributes: Mapped[dict | None] = mapped_column(JSONB)

    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    business: Mapped["Business"] = relationship(back_populates="resources")

    category: Mapped["Category | None"] = relationship(back_populates="resources")

    variants: Mapped[list["BusinessResourceVariant"]] = relationship(
        back_populates="resource",
        cascade="all, delete-orphan",
    )

    leads: Mapped[list["Lead"]] = relationship(
        back_populates="resource",
        passive_deletes=True,
    )


class BusinessResourceVariant(Base, TimestampMixin):
    __tablename__ = "business_resource_variants"

    id: Mapped[int] = mapped_column(primary_key=True)

    resource_id: Mapped[int] = mapped_column(
        ForeignKey("business_resources.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    stock: Mapped[int | None]

    sku: Mapped[str | None] = mapped_column(String(100))

    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    attributes: Mapped[dict | None] = mapped_column(JSONB)

    resource: Mapped["BusinessResource"] = relationship(back_populates="variants")


class KnowledgeDocument(Base, TimestampMixin):
    __tablename__ = "knowledge_documents"

    id: Mapped[int] = mapped_column(primary_key=True)

    business_id: Mapped[int] = mapped_column(
        ForeignKey("businesses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    document_type: Mapped[DocumentType] = mapped_column(SqlEnum(DocumentType), nullable=False)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    business: Mapped["Business"] = relationship(back_populates="knowledge_documents")