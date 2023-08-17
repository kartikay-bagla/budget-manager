from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.savings_goal import SavingsGoal
from app.schemas.savings_goal import SavingsGoalCreate, SavingsGoalUpdate


class CRUDSavingsGoal(CRUDBase[SavingsGoal, SavingsGoalCreate, SavingsGoalUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int | None = 100,
        show_archived: bool = False
    ) -> List[SavingsGoal]:
        if show_archived:
            return super().get_multi(db, skip=skip, limit=limit)
        query = db.query(self.model).filter(
            SavingsGoal.archived == False  # noqa: E712
        ).offset(skip)
        if limit:
            query = query.limit(limit)
        return query.all()

    def create(self, db: Session, *, obj_in: SavingsGoalCreate) -> SavingsGoal:
        db_obj = SavingsGoal(
            name=obj_in.name,
            total_amount=obj_in.total_amount,
            priority=obj_in.priority,
            archived=obj_in.archived,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: SavingsGoal,
        obj_in: Union[SavingsGoalUpdate, Dict[str, Any]]
    ) -> SavingsGoal:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_name(self, db: Session, *, name: str) -> Optional[SavingsGoal]:
        return db.query(self.model).filter(SavingsGoal.name == name).first()


savings_goal = CRUDSavingsGoal(SavingsGoal)
