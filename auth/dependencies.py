from fastapi import Depends, Cookie, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from db import crud
from core.config import settings 
import datetime

def get_current_user(
    session_token: str | None = Cookie(default=None, alias=settings.SESSION_COOKIE_NAME), 
    db: Session = Depends(get_db)
):
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    session = crud.session.get_session_by_token(db, session_token)
    if not session or session.expires_at < datetime.datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session"
        )

    user = crud.user.get_user(db, session.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
