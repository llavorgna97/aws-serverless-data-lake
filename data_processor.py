import os
import logging
import boto3
import pandas as pd
from botocore.exceptions import ClientError

INPUT_BUCKET = os.environ.get("input_bucket")
OUTPUT_BUCKET = os.environ.get("output_bucket")

def lambda_handler(event, context):
    file_name = "cart_abandonment_data.csv"
    download_from_s3(INPUT_BUCKET, file_name)
    aggregated_path = process_data(file_name)
    upload_to_s3(aggregated_path, OUTPUT_BUCKET)
    print(f"✅ Aggregated data uploaded to {OUTPUT_BUCKET}")

def download_from_s3(bucket: str, key: str):
    s3 = boto3.client("s3")
    local_path = f"/tmp/{key}"
    s3.download_file(bucket, key, local_path)
    print(f"Downloaded {key} from {bucket}")

def process_data(file_name: str) -> str:
    local_path = f"/tmp/{file_name}"
    df = pd.read_csv(local_path)
    summary = df.groupby("product_id")["product_amount"].sum().nlargest(50).reset_index()
    summary.columns = ["product_id", "total_abandoned"]
    output_path = "/tmp/cart_aggregated_data.csv"
    summary.to_csv(output_path, index=False)
    print("Processed top 50 products by abandonment count")
    return output_path

def upload_to_s3(file_path: str, bucket: str, object_name=None):
    s3 = boto3.client("s3")
    if object_name is None:
        object_name = os.path.basename(file_path)
    try:
        s3.upload_file(file_path, bucket, object_name)
    except ClientError as e:
        logging.error(f"Error uploading file: {e}")
        raise
