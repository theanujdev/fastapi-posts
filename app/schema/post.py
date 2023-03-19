from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    body: str = Field(min_length=3, max_length=1000)
    author_id: int
    is_published: bool


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True
