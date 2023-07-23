import datetime
import uuid
from typing import Any, List, Optional

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/total", response_model=schemas.TotalExpense)
def total_expenses(
    start_date: datetime.date,
    end_date: datetime.date,
    db: Session = Depends(deps.get_db),
) -> schemas.TotalExpense:
    expenses = crud.expense.get_multi_by_range(
        db=db,
        start_date=start_date,
        end_date=end_date,
    )
    return schemas.TotalExpense(
        total=sum(i.amount for i in expenses)
    )


@router.get("/", response_model=List[schemas.Expense])
def read_expenses(
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None,
    order_by: str = "date",
    order_ascending: bool = False,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve expenses.
    """
    return crud.expense.get_multi_by_range(
        db=db,
        start_date=start_date,
        end_date=end_date,
        order_by=order_by,
        order_ascending=order_ascending,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=list[schemas.Expense])
def create_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_in: schemas.ExpenseCreateAPI,
) -> Any:
    """
    Create new expense.

    Need to resolve recurring_freqency here to generate a list of expenses and then
        create them all.
    """
    cat = crud.category.get(db=db, id=expense_in.category_id)
    # raise error if cat DNE
    if not cat:
        raise HTTPException(
            status_code=400,
            detail="The category with this id does not exist in the system.",
        )

    if not expense_in.is_recurring:
        expense = crud.expense.create(
            db=db,
            obj_in=schemas.ExpenseCreateCRUD(
                category_id=expense_in.category_id,
                description=expense_in.description,
                amount=expense_in.amount,
                date=expense_in.date,
                is_recurring=False,
                recurring_id=None,
            ),
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
        expense = crud.expense.create(
            db=db,
            obj_in=schemas.ExpenseCreateCRUD(
                category_id=expense_in.category_id,
                description=expense_in.description,
                amount=expense_in.amount,
                date=date.date(),
                is_recurring=True,
                recurring_id=recurring_id,
            ),
        )
        expenses.append(expense)
    return expenses


@router.put("/{expense_id}", response_model=schemas.Expense)
def update_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_id: int,
    expense_in: schemas.ExpenseUpdate,
) -> Any:
    """
    Update an expense.
    """
    expense = crud.expense.get(db, id=expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense = crud.expense.update(db, db_obj=expense, obj_in=expense_in)
    return expense


@router.get("/{expense_id}", response_model=schemas.Expense)
def read_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_id: int,
) -> Any:
    """
    Get expense by ID.
    """
    if expense := crud.expense.get(db, id=expense_id):
        return expense
    else:
        raise HTTPException(status_code=404, detail="Expense not found")


@router.delete("/{expense_id}", response_model=schemas.Expense)
def delete_expense(
    *,
    db: Session = Depends(deps.get_db),
    expense_id: int,
) -> Any:
    """
    Delete an expense.
    """
    expense = crud.expense.get(db, id=expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    expense = crud.expense.remove(db=db, id=expense_id)
    return expense
