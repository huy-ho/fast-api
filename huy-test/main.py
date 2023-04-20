from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional, Union
from random import randrange

app = FastAPI()


class Product(BaseModel):
    serialNumber: str
    productFamilyID: str
    customerName: str
    isPartofPF: str = True
    id: int



my_products = [{"serialNumber": "ABC123", "productFamilyID": "ASR9000", "customerName": "AT&T", "id": 1},
            {"serialNumber": "XYZ890", "productFamilyID": "HHH2000", "customerName": "JPMorgan", "id": 2}]


def find_products(id):
    for p in my_products:
        if p["id"] == id:
            return p


def find_index_products(id):
    for i, p in enumerate(my_products):
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
@app.get("/products")
def get_products():
    return {"data": my_products}


@app.post("/products", status_code=status.HTTP_201_CREATED)  # when we create a post, we want a 201 status code
def create_products(prod: Product):
    prod_dict = prod.dict()
    prod_dict['id'] = randrange(0, 1000000)
    my_products.append(prod_dict)
    return {"data": prod_dict}


@app.get("/products/{id}",
         response_model=Union[Product],
         response_model_exclude_none=False)
def get_product(id: int, response: Response):  # int is for validating that it is an integer
    post = find_products(int(id))
    if not post:
        return errorResponse(id)

        #raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        #                   detail=f"post with id: {id} was not found")


        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
    return post


@app.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int):
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_products(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} does not exist")

    my_products.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/products/{id}")
def update_product(id: int, prod: Product):
    index = find_index_products(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    post_dict = prod.dict()
    post_dict['id'] = id
    my_products[index] = post_dict
    return {"data": "updated post"}

