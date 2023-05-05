import datetime
import uuid
from typing import Any, List

import pandas as pd
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
    return crud.expense.get_multi_by_range_and_user(
        db=db,
        user_id=user_id,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=list[schemas.Expense])
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
    if not expense_in.is_recurring:
        expense = crud.expense.create_with_user(
            db=db,
            obj_in=schemas.ExpenseCreateCRUD(
                category_id=expense_in.category_id,
                description=expense_in.description,
                amount=expense_in.amount,
                date=expense_in.date,
                is_recurring=False,
                recurring_id=None,
            ),
            user_id=current_user.id
        )
        return [expense]

    recurring_id = str(uuid.uuid4())
    try:
        assert expense_in.recurring_frequency is not None
        assert expense_in.recurring_start_date is not None
        assert expense_in.recurring_end_date is not None
    except AssertionError as e:
        raise HTTPException(
            status_code=400,
            detail="If is_recurring is True, recurring_frequency, "
            "recurring_start_date, and recurring_end_date must be provided.",
        ) from e
    try:
        date_range: list[datetime.datetime] = pd.date_range(
            start=expense_in.recurring_start_date,
            end=expense_in.recurring_end_date,
            freq=expense_in.recurring_frequency,
        ).to_pydatetime()
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail="Invalid recurring_frequency, recurring_start_date, or "
            "recurring_end_date."
        ) from e
    expenses = []
    for date in date_range:
        expense = crud.expense.create_with_user(
            db=db,
            obj_in=schemas.ExpenseCreateCRUD(
                category_id=expense_in.category_id,
                description=expense_in.description,
                amount=expense_in.amount,
                date=date.date(),
                is_recurring=True,
                recurring_id=recurring_id,
            ),
            user_id=current_user.id,
        )
        expenses.append(expense)
        return expenses


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
