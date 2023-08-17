from datetime import date as date_obj
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class SavingsEntry(Base):
    __tablename__ = "savings_entry"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    savings_goal_id: Mapped[int] = mapped_column(Integer, ForeignKey("savings_goal.id"))
    savings_goal = relationship("SavingsGoal", foreign_keys=[savings_goal_id])
    amount: Mapped[float]
    date: Mapped[date_obj]
