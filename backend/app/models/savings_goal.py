from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class SavingsGoal(Base):
    __tablename__ = "savings_goal"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str]
    total_amount: Mapped[float]
    priority: Mapped[int]
    archived: Mapped[bool] = mapped_column(default=False)
