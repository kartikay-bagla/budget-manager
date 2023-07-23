import datetime as dt
from typing import Any, Dict, Optional, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreateCRUD, ExpenseUpdate


class CRUDExpense(CRUDBase[Expense, ExpenseCreateCRUD, ExpenseUpdate]):
    def update(
        self,
        db: Session,
        *,
        db_obj: Expense,
        obj_in: Union[ExpenseUpdate, Dict[str, Any]],
    ) -> Expense:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi_by_range(
        self,
        db: Session,
        *,
        start_date: Optional[dt.date] = None,
        end_date: Optional[dt.date] = None,
        order_by: str = "date",
        order_ascending: bool = False,
        skip: int = 0,
        limit: Optional[int] = 100,
    ) -> list[Expense]:
        query = db.query(self.model)
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)
        if order_ascending:
            query = query.order_by(order_by)
        else:
            query = query.order_by(desc(order_by))
        query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_total_by_cat_for_range(
        self,
        db: Session,
        *,
        start_date: dt.date,
        end_date: dt.date,
        category_id: int,
    ) -> float:
        expenses = (
            db.query(self.model)
            .filter(
                Expense.date >= start_date,
                Expense.date < end_date,
                Expense.category_id == category_id,
            )
            .all()
        )
        return sum(i.amount for i in expenses)


expense = CRUDExpense(Expense)
