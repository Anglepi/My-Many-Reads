from fastapi import FastAPI

mmr = FastAPI()


@mmr.get("/")
async def root():
    return {"message": "Hello World!"}
