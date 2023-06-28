from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.crud.budget import create_budgets_for_categories

router = APIRouter()


@router.get("/", response_model=List[schemas.Budget])
def read_budgets(
    month: int,
    year: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve budgets for given month.
    """
    if not 1 <= month <= 12:
        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12.",
        )

    return crud.budget.get_multi_by_month(
        db, month=month, year=year, skip=skip, limit=limit
    )


@router.get("/{budget_id}", response_model=schemas.Budget)
def read_budget(
    budget_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve budget by ID.
    """
    if budget := crud.budget.get(db, id=budget_id):
        return budget
    else:
        raise HTTPException(status_code=404, detail="Budget not found")


@router.put("/{budget_id}", response_model=schemas.Budget)
def update_budget(
    budget_id: int,
    budget_in: schemas.BudgetUpdate,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Update a budget.
    """
    budget = crud.budget.get(db, id=budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    budget = crud.budget.update(db, db_obj=budget, obj_in=budget_in)
    return budget


@router.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # 1 day
def create_new_budgets(
    db: Session = Depends(deps.get_db),
    categories: Optional[list[models.Category]] = None,
):
    create_budgets_for_categories(db=db, categories=categories)
