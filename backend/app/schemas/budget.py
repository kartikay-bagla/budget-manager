from pydantic import BaseModel


# Shared properties
class BudgetBase(BaseModel):
    amount: float


# Properties to receive via API on creation
class BudgetCreate(BudgetBase):
    pass


# Properties to receive via API on update
class BudgetUpdate(BudgetBase):
    pass


# Properties stored in DB
class BudgetInDB(BudgetBase):
    id: int
    user_id: int
    category_id: int
    month: int
    year: int

    class Config:
        orm_mode = True


# Properties to return via API
class Budget(BudgetInDB):
    pass
