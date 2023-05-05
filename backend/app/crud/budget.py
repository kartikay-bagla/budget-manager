from typing import Any, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetUpdate


class CRUDBudget(CRUDBase[Budget, BudgetCreate, BudgetUpdate]):
    def create(self, db: Session, *, obj_in: BudgetCreate) -> Budget:
        db_obj = Budget(
            amount=obj_in.amount,
            user_id=obj_in.user_id,
            category_id=obj_in.category_id,
            month=obj_in.month,
            year=obj_in.year
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Budget,
        obj_in: Union[BudgetUpdate, dict[str, Any]]
    ) -> Budget:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi_by_month_and_user(
        self,
        db: Session,
        *,
        month: int,
        year: int,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: Optional[int] = 100
    ) -> list[Budget]:
        query = db.query(self.model)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        query = (
            query
            .filter(self.model.month == month)
            .filter(self.model.year == year)
            .offset(skip)
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_multi_by_range_and_user(
        self,
        db: Session,
        *,
        start_month: int,
        start_year: int,
        end_month: int,
        end_year: int,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: Optional[int] = 100
    ) -> list[Budget]:
        query = db.query(self.model)
        if user_id:
            query = query.filter(self.model.user_id == user_id)
        query = (
            query
            .filter(
                (self.model.year > start_year)
                | ((self.model.year == start_year) & (self.model.month >= start_month))
            )
            .filter(
                (self.model.year < end_year)
                | ((self.model.year == end_year) & (self.model.month <= end_month))
            )
            .offset(skip)
        )
        if limit:
            query = query.limit(limit)
        return query.all()


budget = CRUDBudget(Budget)
