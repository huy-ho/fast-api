from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


# route / path operations

@app.get("/")  # this is a decorator to reference the fastapi. This is a get request
async def root():
    return {"message": "hello world"}


# when you are retrieving data, it is usually a get operations
@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}


@app.post("/createposts")
def create_posts(new_post: Post):
    print(new_post.title)
    return {"data": "new post"}

# we want a title (string)
# we want the content (string)
