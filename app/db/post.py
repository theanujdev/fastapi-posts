from sqlalchemy.orm import Session
from . import models
from ..schema.post import PostCreate


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_posts(db: Session, skip: int, limit: int):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate):
    db_post = models.Post(title=post.title, body=post.body,
                          author_id=post.author_id, is_published=post.is_published)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post: PostCreate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    update_data = post.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    db.commit()
    return db_post


def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return db_post
