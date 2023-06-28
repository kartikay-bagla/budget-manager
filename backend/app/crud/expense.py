import datetime as dt
from typing import Any, Dict, Optional, Union

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
        obj_in: Union[ExpenseUpdate, Dict[str, Any]]
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
        start_date: dt.date,
        end_date: dt.date,
        skip: int = 0,
        limit: Optional[int] = 100
    ) -> list[Expense]:
        query = db.query(self.model).filter(
            Expense.date >= start_date,
            Expense.date <= end_date
        ).offset(skip)
        if limit:
            query = query.limit(limit)
        return query.all()


expense = CRUDExpense(Expense)
