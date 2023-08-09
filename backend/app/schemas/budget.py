from pydantic import BaseModel

from app.schemas.category import Category


# Shared properties
class BudgetBase(BaseModel):
    amount: float


# Properties to receive via API on creation
class BudgetCreate(BudgetBase):
    category_id: int
    month: int
    year: int


# Properties to receive via API on update
class BudgetUpdate(BudgetBase):
    id: int


# Properties stored in DB
class BudgetInDB(BudgetCreate, BudgetUpdate):
    category: Category
    pass

    class Config:
        orm_mode = True


# Properties to return via API
class Budget(BudgetInDB):
    pass


class BudgetWithAmount(Budget):
    expenses: float
    past_expenses: float
    future_expenses: float
