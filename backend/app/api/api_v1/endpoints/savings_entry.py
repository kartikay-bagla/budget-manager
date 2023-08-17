import datetime
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.SavingsEntry])
def read_savings_entries(
    savings_goal_id: int,
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None,
    order_by: str = "date",
    order_ascending: bool = False,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve savings_entries.
    """
    return crud.savings_entry.get_multi_by_range_for_goal(
        db=db,
        savings_goal_id=savings_goal_id,
        start_date=start_date,
        end_date=end_date,
        order_by=order_by,
        order_ascending=order_ascending,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=schemas.SavingsEntry)
def create_savings_entry(
    *,
    db: Session = Depends(deps.get_db),
    savings_entry_in: schemas.SavingsEntryCreateAPI,
) -> Any:
    """Create new savings_entry."""
    savings_goal = crud.savings_goal.get(db=db, id=savings_entry_in.savings_goal_id)
    # raise error if goal DNE
    if not savings_goal:
        raise HTTPException(
            status_code=400,
            detail="The savings goal with this id does not exist in the system.",
        )

    savings_entry = crud.savings_entry.create(
        db=db,
        obj_in=schemas.SavingsEntryCreateCRUD(
            savings_goal_id=savings_entry_in.savings_goal_id,
            amount=savings_entry_in.amount,
            date=savings_entry_in.date,
        ),
    )
    return savings_entry


@router.put("/{savings_entry_id}", response_model=schemas.SavingsEntry)
def update_savings_entry(
    *,
    db: Session = Depends(deps.get_db),
    savings_entry_id: int,
    savings_entry_in: schemas.SavingsEntryUpdate,
) -> Any:
    """
    Update an savings_entry.
    """
    savings_entry = crud.savings_entry.get(db, id=savings_entry_id)
    if not savings_entry:
        raise HTTPException(status_code=404, detail="Savings Entry not found")
    savings_entry = crud.savings_entry.update(
        db, db_obj=savings_entry, obj_in=savings_entry_in
    )
    return savings_entry


@router.get("/{savings_entry_id}", response_model=schemas.SavingsEntry)
def read_savings_entry(
    *,
    db: Session = Depends(deps.get_db),
    savings_entry_id: int,
) -> Any:
    """
    Get savings_entry by ID.
    """
    if savings_entry := crud.savings_entry.get(db, id=savings_entry_id):
        return savings_entry
    else:
        raise HTTPException(status_code=404, detail="Savings Entry not found")


@router.delete("/{savings_entry_id}", response_model=schemas.SavingsEntry)
def delete_savings_entry(
    *,
    db: Session = Depends(deps.get_db),
    savings_entry_id: int,
) -> Any:
    """
    Delete an savings_entry.
    """
    savings_entry = crud.savings_entry.get(db, id=savings_entry_id)
    if not savings_entry:
        raise HTTPException(status_code=404, detail="Savings Entry not found")
    savings_entry = crud.savings_entry.remove(db=db, id=savings_entry_id)
    return savings_entry
