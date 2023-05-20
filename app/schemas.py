from pydantic import BaseModel


class TagUserBase(BaseModel):
    name: str = ""
    negative: bool = False


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


class FollowBase(BaseModel):
    pass


class FollowCreate(FollowBase):
    pass


class Follow(FollowCreate):
    id: int
    user_id: int
    follows_id: int

    class Config:
        orm_mode = True

class LikeBase(BaseModel):
    pass


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    id: int
    post_id: int
    user_id: int

    class Config:
        orm_mode = True


class Post(PostBase):
    id: int
    owner_id: int
    tags: list[TagPost] = []
    photo_url: str = ""
    likes: list[Like] = []

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str = ""


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    posts: list[Post] = []
    tags: list[TagUser] = []
    likes: list[Like] = []
    follower: list[Follow] = []
    following: list[Follow] = []

    class Config:
        orm_mode = True
