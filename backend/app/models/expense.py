from datetime import date as date_obj
from typing import Optional
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Expense(Base):
    __tablename__ = "expense"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"))
    category = relationship("Category", foreign_keys=[category_id])
    description: Mapped[str]
    amount: Mapped[float]
    date: Mapped[date_obj]
    is_recurring: Mapped[bool]
    recurring_id: Mapped[Optional[str]]
