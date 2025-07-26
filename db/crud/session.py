from sqlalchemy.orm import Session
from db.models.session import SessionModel
from datetime import datetime


def get_session_by_token(db: Session, token: str):
    return db.query(SessionModel).filter(SessionModel.token == token).first()


def create_session(db: Session, user_id: int, token: str, expires_at: datetime):
    session = SessionModel(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

