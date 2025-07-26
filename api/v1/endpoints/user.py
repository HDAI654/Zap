from fastapi import Depends, APIRouter
from auth import dependencies

router = APIRouter()

# Simple secure path
@router.get("/me")
def read_me(user=Depends(dependencies.get_current_user)):
    return {"email": user.email, "username": user.username}