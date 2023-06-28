from pydantic import BaseModel


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
    pass

    class Config:
        orm_mode = True


# Properties to return via API
class Budget(BudgetInDB):
    pass
