from fastapi import APIRouter

router = APIRouter()


@router.get("/")
@router.get("/home")
def get_home_page():
    return "<h1>Home Page</h1>"
