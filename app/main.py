from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional, Union
from random import randrange

from starlette.responses import JSONResponse

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # default to true
    rating: Optional[int] = None  # fully optional field, if the user doesn't provide it, it will default to none
    id: int

class ErrorResponse(BaseModel):
    title: str
    content: str
    published: bool = True
    ErrorMessage: str
    ErrorCode: int



my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favorite foods", "content": "i like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


def errorResponse(id):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                       detail=f"post with id: {id} was not found")
# route / path operations

@app.get("/")  # this is a decorator to reference the fastapi. This is a get request
async def root():
    return {"message": "hello world"}


# when you are retrieving data, it is usually a get operations
@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)  # when we create a post, we want a 201 status code
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}",
         response_model=Union[str, Post],
         response_model_exclude_none=False)
def get_post(id: int, response: Response):  # int is for validating that it is an integer
    post = find_post(int(id))
    if not post:
        return errorResponse(id)

        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                   detail=f"post with id: {id} was not found")


        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} does not exist")

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": "updated post"}

