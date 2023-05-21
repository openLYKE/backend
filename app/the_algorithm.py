from sqlalchemy import func, text
from sqlalchemy.orm import Session

import models
import schemas
import crud


def get_random_posts(db: Session):
    ret = db.query(models.Post).order_by(func.random()).limit(100).all()
    for post in ret:
        post.description = "This Post was randomly chosen from all possible posts."
        post.title = "rand"
    return ret


def get_popular_posts(db: Session):
    rs = db.execute(text("""
        select post_id as id, count(post_id) as count from likes
            group by likes.post_id
            order by count(post_id) desc
        """))

    posts = []
    for row in rs:
        post = db.query(models.Post).filter(models.Post.id == row.id).first()
        post.title = "popular"
        post.description = "This Post was chosen because it has a lot of likes in our community."
        posts.append(post)

    return posts


def get_tags_posts(db: Session, tags):
    posts = db.query(models.Post).all()

    ret = []

    for post in posts:
        counter = 0
        post_tags = []
        for tag in tags:
            for posttag in post.tags:
                if tag.name == posttag.name:
                    counter += 1
                    post_tags.append(posttag.name)
        post.title = "tags"
        post.description = "This Post was chosen because it has the tags: " + ", ".join(post_tags) + " and you chose these tags."
        ret.append({"post": post, "count": counter})

    ret.sort(key=lambda x: x["count"], reverse=True)
    return ret


def get_friends_posts(db: Session, user_id: int):
    rs = db.execute(text(f"""
    select p.*
    from posts p, follows f, likes l
    where f.user_id = {user_id}
    and f.follows_id = l.user_id
    and l.post_id = p.id
    """))

    ret = []
    for row in rs:
        ret.append(row.id)

    final = []
    for i in ret:
        post = crud.get_post(db, post_id=i)
        post.title = "friends"
        post.description = "This Post was chosen becaus your friend REPLACEME liked it!"
        final.append(post)

    return final


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

    tags_0, tags_1, tags_2 = seperate_tags(user_tags)

    amount_posts = 100
    posts = []

    if rand != 0.0:
        amount_random_posts = int(amount_posts * rand)
        random_posts = get_random_posts(db)[:amount_random_posts]
        posts += random_posts

    if popular != 0.0:
        amount_popular_posts = int(amount_posts * popular)
        popular_posts = get_popular_posts(db)[:amount_popular_posts]
        posts += popular_posts

    if friends != 0.0:
        amount_friends_posts = int(amount_posts * friends)
        friends_post = get_friends_posts(db, user_id)[:amount_friends_posts]
        posts += friends_post

    if tags != 0.0:
        amount_tag_posts = int(amount_posts * tags)
        tags_posts = get_tags_posts(db, tags_2)[:amount_tag_posts]
        posts += tags_posts

        # if the user has activated tags, we will filter the negative tags

        final = []
        print(f"{posts=}")

        for post in posts:
            # dbtags = db.query(models.TagUser).filter(models.TagUser.owner_id == post.id).all()
            try:
                print(post)
                for tag in post.tags:
                    clean = True
                    for evil_tag in tags_0:
                        if tag.name == evil_tag.name:
                            clean = False
                            break
                    if clean:
                        final.append(post)
            except:
                continue


        print(f"{final=}")

        return final

    return posts
