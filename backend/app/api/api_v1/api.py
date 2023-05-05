from fastapi import APIRouter

from app.api.api_v1.endpoints import budgets, categories, expenses, login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(
    categories.router, prefix="/categories", tags=["categories"]
)
api_router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
