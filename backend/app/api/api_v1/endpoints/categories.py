from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.crud.budget import create_budgets_for_categories

router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve categories.
    """
    return crud.category.get_multi(
        db=db, skip=skip, limit=limit
    )


@router.post("/", response_model=schemas.Category)
def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
) -> Any:
    """
    Create new category.
    """
    category = crud.category.get_by_name(
        db,
        name=category_in.name,
    )
    if category:
        raise HTTPException(
            status_code=400,
            detail="The category with this name already exists in the system.",
        )
    category = crud.category.create(db, obj_in=category_in)
    create_budgets_for_categories(db=db, categories=[category])
    return category


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    category_in: schemas.CategoryUpdate,
) -> Any:
    """
    Update an category.
    """
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail="The category with this ID does not exist in the system.",
        )
    if category.name != category_in.name and crud.category.get_by_name(
        db, name=category_in.name
    ):
        raise HTTPException(
            status_code=400,
            detail="The category with this name already exists in the system.",
        )
    category = crud.category.update(db, db_obj=category, obj_in=category_in)
    return category


@router.get("/{category_id}", response_model=schemas.Category)
def read_category(
    category_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve category by ID.
    """
    return crud.category.get(db, id=category_id)
