from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Budget(Base):
    __tablename__ = "budget"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int]
    category_id: Mapped[int]
    month: Mapped[int]
    year: Mapped[int]
    amount: Mapped[float]
