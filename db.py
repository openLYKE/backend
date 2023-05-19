class User:
    id: int
    username: str

class Post:
    id: int
    type: str
    content: str
    tage: list[str]
    created_at: int
    posted_by: int
    likes: int


