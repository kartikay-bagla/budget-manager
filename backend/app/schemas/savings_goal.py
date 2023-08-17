from pydantic import BaseModel


# Shared properties
class SavingsGoalBase(BaseModel):
    name: str
    total_amount: float
    priority: int
    archived: bool = False


# Properties to receive via API on creation
class SavingsGoalCreate(SavingsGoalBase):
    pass


# Properties to receive via API on update
class SavingsGoalUpdate(SavingsGoalBase):
    pass


# Properties stored in DB
class SavingsGoalInDB(SavingsGoalBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return via API
class SavingsGoal(SavingsGoalInDB):
    pass


class SavingsGoalWithAmount(SavingsGoal):
    amount_saved: float
