from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Budget(Base):
    __tablename__ = "budget"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"))
    category = relationship("Category", foreign_keys=[category_id])
    month: Mapped[int]
    year: Mapped[int]
    amount: Mapped[float]
