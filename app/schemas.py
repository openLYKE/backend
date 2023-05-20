from pydantic import BaseModel


class PostBase(BaseModel):
    title: str = ""
    description: str = ""


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class User(PostBase):
    id: int
    items: list[Post] = []

    class Config:
        orm_mode = True
