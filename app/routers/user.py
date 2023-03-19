from fastapi import APIRouter, Depends, HTTPException, status, Path
from ..schema import user as user_schema
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..db import user as user_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/", response_model=list[user_schema.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_db.get_users(db, skip=skip, limit=limit)


@router.post("/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_db.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    return user_db.create_user(db=db, user=user)


@router.get("/@{username}", response_model=user_schema.User)
def get_user_by_username(username: str = Path(..., max_length=20), db: Session = Depends(get_db)):
    db_user = user_db.get_user_by_username(db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{user_id}", response_model=user_schema.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_db.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=user_schema.User)
def update_user(user_id: int, user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_db.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db.update_user(db=db, user_id=user_id, user=user)


@router.delete("/{user_id}", response_model=user_schema.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_db.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db.delete_user(db=db, user_id=user_id)
