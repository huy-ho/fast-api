from fastapi import FastAPI

app = FastAPI()


#route / path operations

@app.get("/") #this is a decorator to reference the fastapi. This is a get request
async def root():
    return {"message": "interesting"}
