from pydantic import BaseModel
from sqlalchemy import Integer, String, Text, Numeric, DateTime, func
from decimal import Decimal
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""
    pass


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

# Pydantic models
class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float

class ItemUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None