from fastapi import APIRouter
from app.db.dynamodb import get_dynamodb_client
from app.api.v1.models.user_model import UserModel
import uuid

router = APIRouter()

@router.post("/users/create")
async def create_item(user: UserModel):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table("FirstTable")

    item_id = str(uuid.uuid4())  # Generate a unique ID
    item = {"id": item_id, "name": user.name, "description": user.description}

    table.put_item(Item=item)
    return {"message": "Item created", "item": item}

@router.get("/users/item/{item_id}")
async def get_item(item_id: str):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table("FirstTable")

    response = table.get_item(Key={"id": item_id})
    if "Item" in response:
        return response["Item"]
    else:
        return {"message": "Item not found"}

@router.get("/users/list")
async def list_items():
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table("FirstTable")

    response = table.scan()
    items = response.get("Items", [])

    return {"items": items}
#.venv/bin/uvicorn app.main:app --host localhost --port 8000 --reload;
