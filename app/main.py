from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

import uvicorn
import os
import models
import crud
import schemas
from database import engine, SessionLocal

import the_algorithm
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    print(db_user)
    if db_user:
        raise HTTPException(
            status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/feed/{user_id}", response_model=list[schemas.Post])
def feed_user(user_id: int, db: Session = Depends(get_db)):
    posts = crud.get_user_feed(db, user_id=user_id)
    return posts


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/posts/", response_model=schemas.Post)
def create_item_for_user(
        user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
):
    return crud.create_user_post(db=db, post=post, user_id=user_id)


@app.get("/posts/", response_model=list[schemas.Post])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@app.get("/algo/{user_id}")
def test(user_id: int, db: Session = Depends(get_db)):
    return the_algorithm.get_popular_posts(db)


@app.get("/sql")
def sql(db: Session = Depends(get_db)):
    rs = db.execute(text("""
    select post_id as id, count(post_id) as count from likes
        group by likes.post_id
        order by count(post_id) desc
    """))

    ret = []
    for row in rs:
        ret.append({"id": row.id, "count": row.count})
    return ret


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv(
        "PORT", default=8000), log_level="info")
