import datetime as dt
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.tasks import repeat_every
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
        db, month=month, year=year, user_id=user_id, skip=skip, limit=limit
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


def _get_if_budget_exist_else_create(
    db: Session, cat: models.Category, month: int, year: int
) -> models.Budget:
    budget = crud.budget.get_by_kwargs(
        db=db, category_id=cat.id, month=month, year=year
    )
    if len(budget) != 0:
        return budget[0]
    # TODO: Add log saying creating budget.
    return crud.budget.create(
        db=db,
        obj_in=schemas.BudgetCreate(
            amount=cat.default_budget_amount,
            user_id=cat.user_id,
            category_id=cat.id,
            month=month,
            year=year,
        ),
    )


@router.on_event("startup")
@repeat_every(seconds=60 * 60 * 24)  # 1 day
def create_new_budgets(db: Session = Depends(deps.get_db)):
    """Create current and next month for all categories of all users."""
    dates = [dt.datetime.now(), dt.datetime.now() + dt.timedelta(days=1)]
    for current_date in dates:
        categories = crud.category.get_multi(db=db)
        for cat in categories:
            _get_if_budget_exist_else_create(
                db=db, cat=cat, month=current_date.month, year=current_date.year
            )
