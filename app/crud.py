from sqlalchemy.orm import Session

import models
import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    db_item = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_tags(db: Session, skip: int = 0, limit: int = 100):
    finaltags = []
    usertags = db.query(models.TagUser).offset(skip).limit(limit).all()
    posttags = db.query(models.TagPost).offset(skip).limit(limit).all()


def update_user_tags(db: Session, user_id: int, tags: schemas.TagUser):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    tag_in_user = False
    for tag in db_user.tags:
        if tag.name == tags.name:
            tag_in_user = True
            break

    if not tag_in_user:
        db_user.tags.append(tags)
        db.commit()
        db.refresh(db_user)
        return db_user

    db.query(models.TagUser).filter(models.TagUser.name == tags.name).update({models.TagUser.is_evil: tags.name}, synchronize_session=False)

    
    return db_user