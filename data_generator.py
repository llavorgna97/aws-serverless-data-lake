from faker import Faker
import random
import logging
import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd

INPUT_BUCKET = os.environ.get("input_bucket")

def lambda_handler(event, context):
    file_path = "/tmp/cart_abandonment_data.csv"
    generate_fake_dataset(file_path)
    upload_to_s3(file_path, INPUT_BUCKET)
    print(f"✅ File uploaded to {INPUT_BUCKET}")

def generate_fake_dataset(file_path: str):
    fake = Faker()
    data = {
        "cart_id": [random.randint(1, 20) for _ in range(1000)],
        "customer_id": [random.randint(1, 50) for _ in range(1000)],
        "product_id": [random.randint(1, 30) for _ in range(1000)],
        "product_amount": [random.randint(1, 10) for _ in range(1000)],
        "product_price": [round(random.uniform(5, 200), 2) for _ in range(1000)],
    }
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    print(f"Generated dataset with {len(df)} rows")

def upload_to_s3(file_path: str, bucket: str, object_name=None):
    s3 = boto3.client("s3")
    if object_name is None:
        object_name = os.path.basename(file_path)
    try:
        s3.upload_file(file_path, bucket, object_name)
    except ClientError as e:
        logging.error(f"Error uploading file: {e}")
        raise
