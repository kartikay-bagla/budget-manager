from pydantic import BaseModel


# Shared properties
class CategoryBase(BaseModel):
    name: str
    default_budget_amount: float
    user_id: int


# Properties to receive via API on creation
class CategoryCreate(CategoryBase):
    pass


# Properties to receive via API on update
class CategoryUpdate(CategoryBase):
    pass


# Properties stored in DB
class CategoryInDB(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return via API
class Category(CategoryInDB):
    pass
