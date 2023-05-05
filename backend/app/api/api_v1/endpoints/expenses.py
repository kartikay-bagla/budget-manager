import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Expense])
def read_expenses(
    start_date: datetime.date,
    end_date: datetime.date,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve expenses.
    """
    user_id = None if current_user.is_superuser else current_user.id
    # TODO: Create get_multi_by_range_and_user.
    return crud.expense.get_multi_by_range_and_user(
        db=db,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=schemas.Expense)
def create_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_in: schemas.ExpenseCreateAPI,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new expense.

    Need to resolve recurring_freqency here to generate a list of expenses and then
        create them all.
    """
    # TODO: Add recurring expenses logic.
    expense = crud.expense.create_with_user(
        db=db, obj_in=expense_in, user_id=current_user.id
    )
    return expense


@router.put("/{expense_id}", response_model=schemas.Expense)
def update_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_id: int,
    expense_in: schemas.ExpenseUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an expense.
    """
    expense = crud.expense.get(db, id=expense_id)
    if not expense or expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense = crud.expense.update(db, db_obj=expense, obj_in=expense_in)
    return expense


@router.get("/{expense_id}", response_model=schemas.Expense)
def read_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get expense by ID.
    """
    expense = crud.expense.get(db, id=expense_id)
    if not expense or expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@router.delete("/{expense_id}", response_model=schemas.Expense)
def delete_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an expense.
    """
    expense = crud.expense.get(db, id=expense_id)
    if not expense or expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense = crud.expense.remove(db=db, id=expense_id)
    return expense
