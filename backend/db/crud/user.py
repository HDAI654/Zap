from sqlalchemy.orm import Session
from db.models.user import UserModel
import datetime

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def create_user(db: Session, email: str, hashed_password: str, username: str):
    user = UserModel(
        email=email,
        hashed_password=hashed_password,
        username=username,
        is_active=True,
        created_at=datetime.datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
