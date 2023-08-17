import datetime as dt
from typing import Any, Dict, Optional, Union

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.savings_entry import SavingsEntry
from app.schemas.savings_entry import SavingsEntryCreateCRUD, SavingsEntryUpdate


class CRUDSavingsEntry(
    CRUDBase[SavingsEntry, SavingsEntryCreateCRUD, SavingsEntryUpdate]
):
    def update(
        self,
        db: Session,
        *,
        db_obj: SavingsEntry,
        obj_in: Union[SavingsEntryUpdate, Dict[str, Any]],
    ) -> SavingsEntry:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi_by_range_for_goal(
        self,
        db: Session,
        *,
        savings_goal_id: int,
        start_date: Optional[dt.date] = None,
        end_date: Optional[dt.date] = None,
        order_by: str = "date",
        order_ascending: bool = False,
        skip: int = 0,
        limit: Optional[int] = 100,
    ) -> list[SavingsEntry]:
        query = db.query(self.model).filter(
            SavingsEntry.savings_goal_id == savings_goal_id
        )
        if start_date:
            query = query.filter(SavingsEntry.date >= start_date)
        if end_date:
            query = query.filter(SavingsEntry.date < end_date)
        order_by_obj = order_by if order_ascending else desc(order_by)
        query = query.order_by(order_by_obj, desc("amount"))  # type: ignore
        query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_total_by_goal_for_range(
        self,
        db: Session,
        *,
        savings_goal_id: int,
        start_date: Optional[dt.date] = None,
        end_date: Optional[dt.date] = None,
    ) -> float:
        query = db.query(self.model).filter(
            SavingsEntry.savings_goal_id == savings_goal_id,
        )
        if start_date:
            query = query.filter(SavingsEntry.date >= start_date)
        if end_date:
            query = query.filter(SavingsEntry.date < end_date)
        return sum(i.amount for i in query.all())


savings_entry = CRUDSavingsEntry(SavingsEntry)
