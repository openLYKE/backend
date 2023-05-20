from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    posts = relationship("Post", back_populates="owner")
    tags = relationship("TagUser", back_populates="owner")
    likes = relationship("Like", back_populates="user")
    follower = relationship("Follow", back_populates="follows", foreign_keys="Follow.follows_id")
    following = relationship("Follow", back_populates="user", foreign_keys="Follow.user_id")


class Follow(Base):
    __tablename__ = "follows"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    follows_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="follower", foreign_keys=[user_id])
    follows = relationship("User", back_populates="following", foreign_keys=[follows_id])




class TagUser(Base):
    __tablename__ = "tags_user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    preference = Column(Integer, index=True, default=1)  # 1 = neutral, 0 = negative, 2: positive
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tags")


class TagPost(Base):
    __tablename__ = "tags_post"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("posts.id"))
    owner = relationship("Post", back_populates="tags")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    photo_url = Column(String(255), index=True, default="https://images.lmu.social/42.jpg")
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")
    tags = relationship("TagPost", back_populates="owner")
    likes = relationship("Like", back_populates="post")


class Like(Base):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="likes")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="likes")