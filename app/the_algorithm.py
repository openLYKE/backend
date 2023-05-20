from sqlalchemy import func
from sqlalchemy.orm import Session

import models
import schemas


def get_random_posts(db: Session):
    return db.query(models.Post).order_by(func.random()).limit(100).all()


def get_popular(db: Session):
    pass


def get_posts_from_tag(db: Session, user_id: int):
    posts = db.query(models.Post).all()
    tags = db.query(models.TagUser).filter(models.TagUser.owner_id == user_id).all()

    hashmap = {}

    for post in posts:
        counter = 0
        for tag in tags:
            if tag in post.tags:
                counter += 1
        hashmap[post] = counter

    print(hashmap)

    return hashmap


def algo(rand: float, popular: float, friends: float, tags: float):
    COUNT = 100
