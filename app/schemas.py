from pydantic import BaseModel



class TagUserBase(BaseModel):
    name: str = ""


class TagUserCreate(TagUserBase):
    pass


class TagUser(TagUserCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class TagPostBase(BaseModel):
    name: str = ""


class TagPostCreate(TagPostBase):
    pass


class TagPost(TagPostCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str = ""
    description: str = ""


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int
    tags: list[TagPost] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    posts: list[Post] = []
    tags: list[TagUser] = []

    class Config:
        orm_mode = True
