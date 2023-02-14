from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


# route / path operations

@app.get("/")  # this is a decorator to reference the fastapi. This is a get request
async def root():
    return {"message": "hello world"}


# when you are retrieving data, it is usually a get operations
@app.get("/posts")
def get_posts():
    return {"data": "This is your posts"}

@app.post("/createposts")
def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return {"new_post": f"title: {payLoad['title']} content: {payLoad['content']}"}
