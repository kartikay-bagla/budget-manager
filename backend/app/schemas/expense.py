from datetime import date as date_obj
from typing import Optional
from pydantic import BaseModel


# Shared properties
class ExpenseBase(BaseModel):
    category_id: int
    description: str
    amount: float
    date: date_obj


class ExpenseRecurring(BaseModel):
    is_recurring: bool


# Properties to send to crud
class ExpenseCreateCRUD(ExpenseBase, ExpenseRecurring):
    recurring_id: Optional[str]


# Properties to receive via API on creation
class ExpenseCreateAPI(ExpenseBase, ExpenseRecurring):
    recurring_start_date: Optional[date_obj]
    recurring_end_date: Optional[date_obj]
    recurring_frequency: Optional[str]


# Properties to receive via API on update
class ExpenseUpdate(ExpenseBase):
    pass


# Properties stored in DB
class ExpenseInDB(ExpenseCreateCRUD):
    id: int

    class Config:
        orm_mode = True


# Properties to return via API
class Expense(ExpenseInDB):
    pass
