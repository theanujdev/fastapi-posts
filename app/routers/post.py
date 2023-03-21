from fastapi import APIRouter, Depends, HTTPException, status
from ..schema import post as post_schema
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..db import post as post_db
from ..auth.oauth2 import get_current_active_user
from ..db import models

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("/", response_model=list[post_schema.Post])
def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return post_db.get_posts(db, skip=skip, limit=limit)


@router.post("/", response_model=post_schema.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: post_schema.PostCreate, user: models.User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    return post_db.create_post(db=db, post=post, author_id=user.id)


@router.get("/{post_id}", response_model=post_schema.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = post_db.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.put("/{post_id}", response_model=post_schema.Post)
def update_post(post_id: int, post: post_schema.PostCreate, db: Session = Depends(get_db)):
    db_post = post_db.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_db.update_post(db=db, post_id=post_id, post=post)


@router.delete("/{post_id}", response_model=post_schema.Post)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = post_db.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_db.delete_post(db=db, post_id=post_id)
