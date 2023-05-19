from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return "openLYKE API go brrrr"

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/user/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/post/{post_id}")
async def get_post(post_id: int):
    return {"post_id": post_id}

@app.get("/finn")
async def kick_finn():
    # Increment kick finn counter
    return {"message": "Finn has been kicked"}
