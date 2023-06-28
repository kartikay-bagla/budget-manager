from fastapi import APIRouter

from app.api.api_v1.endpoints import budgets, categories, expenses

api_router = APIRouter()
api_router.include_router(budgets.router, prefix="/budgets", tags=["budgets"])
api_router.include_router(
    categories.router, prefix="/categories", tags=["categories"]
)
api_router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])


@api_router.get("/healthcheck")
def health_check():
    """Health check endpoint."""
    return "ok"
