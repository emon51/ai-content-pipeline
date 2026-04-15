"""S3/MinIO storage service for uploading JSON files."""

import json
import boto3
from django.conf import settings


def get_s3_client():
    """Create and return a boto3 S3 client using Django settings."""
    return boto3.client(
        "s3",
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )


def upload_json(key: str, data: dict) -> str:
    """
    Serialize and upload a dict as a JSON file to S3/MinIO.

    Args:
        key: S3 object key (e.g. 'rentbyowner.com/details/input/input.json')
        data: Python dict to serialize and upload.

    Returns:
        The S3 key of the uploaded object.

    Raises:
        botocore.exceptions.ClientError: On S3 upload failure.
    """
    client = get_s3_client()

    client.put_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=key,
        Body=json.dumps(data, indent=2),
        ContentType="application/json",
    )

    return key