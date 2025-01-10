import boto3
import os
from dotenv import load_dotenv


def get_dynamodb_client():
    # Load credentials from environment variables
    load_dotenv()
    aws_access_key_id = os.getenv("PRACTICE_AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("PRACTICE_AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("PRACTICE_AWS_REGION", "eu-north-1")  # Default region

    print(aws_secret_access_key)
    return boto3.resource(
        'dynamodb',
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
