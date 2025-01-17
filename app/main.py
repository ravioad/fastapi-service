from fastapi import FastAPI
from app.api.v1.routes import router as api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def read_root():
    return {"message": "Welcome to OUR FastAPI service!"}

#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int, q: str = None):
#     return {"item_id": item_id, "query": q}