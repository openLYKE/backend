from sqlalchemy import func, text
from sqlalchemy.orm import Session

import models
import schemas


def get_random_posts(db: Session):
    return db.query(models.Post).order_by(func.random()).limit(100).all()


def get_popular_posts(db: Session):
    rs = db.execute(text("""
        select post_id as id, count(post_id) as count from likes
            group by likes.post_id
            order by count(post_id) desc
        """))

    posts = []
    for row in rs:
        posts.append(db.query(models.Post).filter(models.Post.id == row.id).first())

    return posts


def get_posts_from_tag(db: Session, user_id: int):
    print("ALGO")
    posts = db.query(models.Post).all()
    tags = db.query(models.TagUser).filter(models.TagUser.owner_id == user_id).all()

    ret = []

    for post in posts:
        counter = 0
        for tag in tags:
            for posttag in post.tags:
                if tag.name == posttag.name:
                    counter += 1
        ret.append({"post": post, "count": counter})

    print(ret)

    ret.sort(key=lambda x: x["count"], reverse=True)

    print(ret)

    return ret


def get_post_from_friends():
    pass


def get_friends_posts(db):
    pass


def algo(db, user_id, rand: float, popular: float, friends: float, tags: float):
    COUNT = 100
    posts = []

    if (rand != 0):
        random_posts = get_random_posts(db)

        posts.append(random_posts)

    if (popular != 0):
        popular_posts = get_popular_posts(db)


        posts.append(popular_posts)

    if (friends != 0):
        friends_post = get_friends_posts(db)


        posts.append(popular_posts)

    if (tags != 0):
        tags_posts = get_posts_from_tag(db, user_id)

        posts.append(tags_posts)


        for post in posts:
            if post.tags


        pass
