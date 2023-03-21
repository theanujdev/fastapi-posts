from sqlalchemy.orm import Session
from . import models
from ..schema.user import UserCreate
from ..auth.hash import Hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int, limit: int):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    db_user = models.User(username=user.username,
                          password=Hash.hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    return db_user


# def update_user(db: Session, user_id: int, user: UserCreate):
#     db.query(models.User).filter(
#         models.User.id == user_id).update(user.dict())
#     db.commit()
#     return db.query(models.User).filter(models.User.id == user_id).first()


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user
