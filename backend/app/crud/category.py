from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    def create(self, db: Session, *, obj_in: CategoryCreate) -> Category:
        db_obj = Category(
            name=obj_in.name,
            default_budget_amount=obj_in.default_budget_amount,
            user_id=obj_in.user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Category,
        obj_in: Union[CategoryUpdate, Dict[str, Any]]
    ) -> Category:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi_by_user(
        self,
        db: Session,
        *,
        user_id: Optional[int] = None,
        skip: int = 0,
        limit: Optional[int] = 100
    ) -> list[Category]:
        query = db.query(self.model)
        if user_id:
            query = query.filter(Category.user_id == user_id)
        query = query.offset(skip)
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_by_name(
        self,
        db: Session,
        *,
        name: str,
        user_id: Optional[int] = None
    ) -> Optional[Category]:
        query = db.query(self.model).filter(Category.name == name)
        if user_id:
            query = query.filter(Category.user_id == user_id)
        return query.first()


category = CRUDCategory(Category)
