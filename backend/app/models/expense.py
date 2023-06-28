from datetime import date as date_obj
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Expense(Base):
    __tablename__ = "expense"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    category_id: Mapped[int]
    description: Mapped[str]
    amount: Mapped[float]
    date: Mapped[date_obj]
    is_recurring: Mapped[bool]
    recurring_id: Mapped[Optional[str]]
