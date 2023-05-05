from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Budget])
def read_budgets(
    month: int,
    year: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve budgets for given month for the user.

    If the user is a superuser, retrieve all budgets for the given month.
    """
    if 1 <= month <= 12:
        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12.",
        )

    user_id = None if current_user.is_superuser else current_user.id

    return crud.budget.get_multi_by_month_and_user(
        db,
        month=month,
        year=year,
        user_id=user_id,
        skip=skip,
        limit=limit
    )


@router.get("/{budget_id}", response_model=schemas.Budget)
def read_budget(
    budget_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve budget by ID.
    """
    budget = crud.budget.get(db, id=budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    if budget.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return budget


@router.put("/{budget_id}", response_model=schemas.Budget)
def update_budget(
    budget_id: int,
    budget_in: schemas.BudgetUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a budget.
    """
    budget = crud.budget.get(db, id=budget_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    if budget.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    budget = crud.budget.update(db, db_obj=budget, obj_in=budget_in)
    return budget
