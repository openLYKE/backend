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


def get_tags_posts(db: Session, tags):
    posts = db.query(models.Post).all()

    ret = []

    for post in posts:
        counter = 0
        for tag in tags:
            for posttag in post.tags:
                if tag.name == posttag.name:
                    counter += 1
        ret.append({"post": post, "count": counter})

    ret.sort(key=lambda x: x["count"], reverse=True)
    return ret


def get_friends_posts(db):
    pass


def seperate_tags(tags: list[schemas.TagUser]):
    tags_0 = []
    tags_1 = []
    tags_2 = []

    for tag in tags:
        if tag.preference == 0:
            tags_0.append(tag)
        elif tag.preference == 1:
            tags_1.append(tag)
        elif tag.preference == 2:
            tags_2.append(tag)

    return tags_0, tags_1, tags_2


def recommender_system(db, user_id, rand: float, popular: float, friends: float, tags: float):
    user_tags = db.query(models.TagUser).filter(models.TagUser.owner_id == user_id).all()

    tags_0, tags_1, tags_2  = seperate_tags(user_tags)

    amount_posts = 100
    posts = []

    if rand != 0:
        amount_random_posts = int(amount_posts * rand)
        random_posts = get_random_posts(db)[:amount_random_posts]
        posts.append(random_posts)

    if popular != 0:
        amount_popular_posts = int(amount_posts * popular)
        popular_posts = get_popular_posts(db)[:amount_popular_posts]
        posts.append(popular_posts)

    if friends != 0:
        amount_friends_posts = int(amount_posts * friends)
        friends_post = get_friends_posts(db)[:amount_friends_posts]
        posts.append(friends_post)

    if tags != 0:
        amount_tag_posts = int(amount_posts * tags)
        tags_posts = get_tags_posts(db, tags_2)[:amount_tag_posts]
        posts.append(tags_posts)

        # if the user has activated tags, we will filter the negative tags

        final = []

        for post in posts:
            for tag in post.tags:
                clean = True
                for evil_tag in tags_0:
                    if tag.name == evil_tag.name:
                        clean = False
                        break
                if clean:
                    final.append(post)




    return final