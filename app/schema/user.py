from pydantic import BaseModel, Field
from .post import Post


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=20)


class UserCreate(UserBase):
    password: str = Field(min_length=3, max_length=20)


class User(UserBase):
    id: int
    posts: list[Post] = []

    class Config:
        orm_mode = True
