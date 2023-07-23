from typing import Any, List, Optional
import datetime as dt

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.crud.budget import create_budgets_for_categories

router = APIRouter()


def get_full_budget_data(db: Session, budget: models.Budget):
    sd = dt.date(year=budget.year, month=budget.month, day=1)
    ed = sd + relativedelta(months=1)
    total_expenses = crud.expense.get_total_by_cat_for_range(
        db=db, start_date=sd, end_date=ed, category_id=budget.category_id
    )
    return schemas.BudgetWithAmount(
        amount=budget.amount,
        id=budget.id,
        category_id=budget.category_id,
        month=budget.month,
        year=budget.year,
        category=budget.category,
        expenses=total_expenses,
    )


@router.get("/", response_model=List[schemas.BudgetWithAmount])
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

    create_budgets_for_categories(db=db, categories=None)

    budgets = crud.budget.get_multi_by_month(
        db, month=month, year=year, skip=skip, limit=limit
    )
    return [get_full_budget_data(db=db, budget=budget) for budget in budgets]


@router.get("/{budget_id}", response_model=schemas.BudgetWithAmount)
def read_budget(
    budget_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve budget by ID.
    """
    if budget := crud.budget.get(db, id=budget_id):
        return get_full_budget_data(db=db, budget=budget)
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
