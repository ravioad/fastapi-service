from app.db.dynamodb import get_dynamodb_client

def create_table():
    dynamoDb = get_dynamodb_client()

    table_name = "FirstTable"  # Example table name
    existing_tables = dynamoDb.meta.client.list_tables()["TableNames"]
    print(existing_tables)
    if table_name not in existing_tables:
        table = dynamoDb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"},  # Partition key
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"},  # String type
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        )
        print(f"Creating table: {table_name}")
        table.wait_until_exists()
    else:
        print(f"Table {table_name} already exists.")
    existing_tables = dynamoDb.meta.client.list_tables()["TableNames"]
    print(existing_tables)


if __name__ == "__main__":
    create_table()