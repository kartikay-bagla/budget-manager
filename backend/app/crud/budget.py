import datetime as dt
from typing import Any, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.crud.category import category
from app.models.budget import Budget
from app.models.category import Category
from app.schemas.budget import BudgetCreate, BudgetUpdate


class CRUDBudget(CRUDBase[Budget, BudgetCreate, BudgetUpdate]):
    def create(self, db: Session, *, obj_in: BudgetCreate) -> Budget:
        db_obj = Budget(
            amount=obj_in.amount,
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

    def get_multi_by_month(
        self,
        db: Session,
        *,
        month: int,
        year: int,
        skip: int = 0,
        limit: Optional[int] = 100
    ) -> list[Budget]:
        query = (
            db.query(self.model)
            .filter(self.model.month == month)
            .filter(self.model.year == year)
            .offset(skip)
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_multi_by_range(
        self,
        db: Session,
        *,
        start_month: int,
        start_year: int,
        end_month: int,
        end_year: int,
        skip: int = 0,
        limit: Optional[int] = 100
    ) -> list[Budget]:
        query = (
            db.query(self.model)
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


def _get_if_budget_exist_else_create(
    db: Session, cat: Category, month: int, year: int
) -> Budget:
    budget_obj = budget.get_by_kwargs(
        db=db, category_id=cat.id, month=month, year=year
    )
    if len(budget_obj) != 0:
        return budget_obj[0]
    # TODO: Add log saying creating budget.
    return budget.create(
        db=db,
        obj_in=BudgetCreate(
            amount=cat.default_budget_amount,
            category_id=cat.id,
            month=month,
            year=year,
        ),
    )


def create_budgets_for_categories(
    db: Session,
    categories: Optional[list[Category]] = None,
):
    """
    Create budgets for given categories.

    If categories is None, create for all categories.
    """
    if categories is None:
        categories = category.get_multi(db=db)

    cd = dt.datetime.now()
    td = dt.timedelta(days=1)
    dates = [cd - td, cd, cd + td]

    for current_date in dates:
        for cat in categories:
            _get_if_budget_exist_else_create(
                db=db, cat=cat, month=current_date.month, year=current_date.year
            )
