from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import uvicorn
import os
import models
import crud
import schemas
from database import engine, SessionLocal

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


@app.put("/users/{user_id}/tags")
def update_user_tags(user_id: int, tag: schemas.TagUser, db: Session = Depends(get_db)):
    return crud.update_user_tags(db=db, user_id=user_id, tags=tag)


@app.get("/posts/", response_model=list[schemas.Post])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_posts(db, skip=skip, limit=limit)
    return items


@app.get("/tags/{tag_id}", response_model=list[schemas.TagUser | schemas.TagPost])
def read_tags(tag_id: int, db: Session = Depends(get_db)):
    items = crud.get_tags(db, skip=0, limit=42069)
    return items

@app.get("/sql")
def sql(db: Session = Depends(get_db)):
    return db.execute("SELECT * FROM users")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv(
        "PORT", default=8000), log_level="info")
