from fastapi import APIRouter

from app.api.v1.models.update_user_model import UpdateUserModel
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


@router.put("/users/update/{item_id}")
async def update_item(item_id: str, user: UpdateUserModel):
    dynamodb = get_dynamodb_client()
    table = dynamodb.Table("FirstTable")

    # Build the UpdateExpression dynamically based on provided fields
    update_expression = []
    expression_attribute_names = {}
    expression_attribute_values = {}

    if user.name is not None:
        update_expression.append("#name = :name")
        expression_attribute_names["#name"] = "name"
        expression_attribute_values[":name"] = user.name

    if user.description is not None:
        update_expression.append("#description = :description")
        expression_attribute_names["#description"] = "description"
        expression_attribute_values[":description"] = user.description

    if not update_expression:
        return {"message": "No fields provided for update"}

    try:
        response = table.update_item(
            Key={"id": item_id},
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW",
        )
        return {"message": "Item updated successfully", "updated_attributes": response.get("Attributes", {})}
    except Exception as e:
        return {"message": "Error updating item", "error": str(e)}



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
# .venv/bin/uvicorn app.main:app --host localhost --port 8000 --reload;
