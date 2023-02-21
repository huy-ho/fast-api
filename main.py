from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default to true
    rating: Optional[int] = None  # fully optional field, if the user doesn't provide it, it will default to none


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "i like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p



# route / path operations

@app.get("/")  # this is a decorator to reference the fastapi. This is a get request
async def root():
    return {"message": "hello world"}


# when you are retrieving data, it is usually a get operations
@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):  # int is for validating that it is an integer
    post = find_post(int(id))
    return {"post_detail": post}
