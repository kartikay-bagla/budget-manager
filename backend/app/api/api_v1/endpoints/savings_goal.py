from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


def get_full_savings_goal(
    db: Session, savings_goal: models.SavingsGoal
) -> schemas.SavingsGoalWithAmount:
    return schemas.SavingsGoalWithAmount(
        id=savings_goal.id,
        name=savings_goal.name,
        total_amount=savings_goal.total_amount,
        priority=savings_goal.priority,
        archived=savings_goal.archived,
        amount_saved=crud.savings_entry.get_total_by_goal_for_range(
            db=db, savings_goal_id=savings_goal.id
        ),
    )


@router.get("/", response_model=List[schemas.SavingsGoalWithAmount])
def read_savings_goals(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve savings_goals.
    """
    goals = crud.savings_goal.get_multi(db=db, skip=skip, limit=limit)
    return [get_full_savings_goal(db=db, savings_goal=goal) for goal in goals]


@router.post("/", response_model=schemas.SavingsGoal)
def create_savings_goal(
    *,
    db: Session = Depends(deps.get_db),
    savings_goal_in: schemas.SavingsGoalCreate,
) -> Any:
    """
    Create new savings_goal.
    """
    savings_goal = crud.savings_goal.get_by_name(
        db,
        name=savings_goal_in.name,
    )
    if savings_goal:
        raise HTTPException(
            status_code=400,
            detail="The savings_goal with this name already exists in the system.",
        )
    savings_goal = crud.savings_goal.create(db, obj_in=savings_goal_in)
    return savings_goal


@router.put("/{savings_goal_id}", response_model=schemas.SavingsGoal)
def update_savings_goal(
    *,
    db: Session = Depends(deps.get_db),
    savings_goal_id: int,
    savings_goal_in: schemas.SavingsGoalUpdate,
) -> Any:
    """
    Update an savings_goal.
    """
    savings_goal = crud.savings_goal.get(db, id=savings_goal_id)
    if not savings_goal:
        raise HTTPException(
            status_code=404,
            detail="The savings_goal with this ID does not exist in the system.",
        )
    if savings_goal.name != savings_goal_in.name and crud.savings_goal.get_by_name(
        db, name=savings_goal_in.name
    ):
        raise HTTPException(
            status_code=400,
            detail="The savings_goal with this name already exists in the system.",
        )
    savings_goal = crud.savings_goal.update(
        db, db_obj=savings_goal, obj_in=savings_goal_in
    )
    return savings_goal


@router.get("/{savings_goal_id}", response_model=schemas.SavingsGoalWithAmount)
def read_savings_goal(
    savings_goal_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve savings_goal by ID.
    """
    goal = crud.savings_goal.get(db, id=savings_goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Savings Goal not found")
    return get_full_savings_goal(
        db=db, savings_goal=goal
    )
