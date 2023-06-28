from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str]
    default_budget_amount: Mapped[float]
