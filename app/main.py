from fastapi import FastAPI
from .routers import blog, user

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
