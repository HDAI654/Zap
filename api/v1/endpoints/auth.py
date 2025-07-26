from fastapi import Depends, Response, APIRouter
from sqlalchemy.orm import Session
from db.session import get_db
from auth import security, session_manager
from db import crud
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from core.config import settings

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

class LoginSchema(BaseModel):
    email: str
    password: str

# simple register

@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    hashed = security.hash_password(data.password)
    user = crud.user.create_user(
        db,
        email=data.email,
        hashed_password=hashed,
        username=data.username
    )
    return {"msg": "User created", "user_id": user.id}

# simple login
@router.post("/login")
def login(data: LoginSchema, response: Response, db: Session = Depends(get_db)):
    user = crud.user.get_user_by_email(db, data.email)
    if not user or not security.verify_password(data.password, user.hashed_password):
        return {"error": "Invalid credentials"}

    token = session_manager.create_session_token()
    expires_at = datetime.utcnow() + timedelta(minutes=60)

    crud.session.create_session(db, user.id, token, expires_at)
    session_manager.set_session_cookie(response, token)
    return {"msg": "Login successful"}
