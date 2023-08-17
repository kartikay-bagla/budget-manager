from datetime import date as date_obj
from pydantic import BaseModel

from app.schemas.savings_goal import SavingsGoal


# Shared properties
class SavingsEntryBase(BaseModel):
    savings_goal_id: int
    amount: float
    date: date_obj


# Properties to send to crud
class SavingsEntryCreateCRUD(SavingsEntryBase):
    pass


# Properties to receive via API on creation
class SavingsEntryCreateAPI(SavingsEntryBase):
    pass


# Properties to receive via API on update
class SavingsEntryUpdate(SavingsEntryBase):
    pass


# Properties stored in DB
class SavingsEntryInDB(SavingsEntryCreateCRUD):
    id: int
    savings_goal: SavingsGoal

    class Config:
        orm_mode = True


# Properties to return via API
class SavingsEntry(SavingsEntryInDB):
    pass
