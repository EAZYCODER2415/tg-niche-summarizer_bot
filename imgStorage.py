import os
import boto3

# Initialize S3 Client for Cloudflare R2
s3 = boto3.client(
    "s3",
    endpoint_url=f"https://{os.getenv('R2_ACCOUNT_ID')}.r2.cloudflarestorage.com",
    aws_access_key_id=os.getenv("R2_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("R2_SECRET_ACCESS_KEY"),
)

MAX_BUCKET_SIZE_BYTES = 8 * 1024 * 1024 * 1024  # 8 GB threshold (Safety Buffer)

def get_bucket_total_size(bucket_name: str) -> int:
    """Calculates total storage consumed by the bucket in bytes."""
    total_bytes = 0
    paginator = s3.get_paginator("list_objects_v2")
    
    for page in paginator.paginate(Bucket=bucket_name):
        if "Contents" in page:
            for obj in page["Contents"]:
                total_bytes += obj["Size"]
    return total_bytes

def delete_oldest_objects(bucket_name: str, target_freed_bytes: int):
    """Deletes the oldest objects to free up storage space."""
    paginator = s3.get_paginator("list_objects_v2")
    objects = []

    for page in paginator.paginate(Bucket=bucket_name):
        if "Contents" in page:
            objects.extend(page["Contents"])

    # Sort objects by LastModified timestamp (Oldest first)
    objects.sort(key=lambda x: x["LastModified"])

    freed = 0
    for obj in objects:
        if freed >= target_freed_bytes:
            break
        s3.delete_object(Bucket=bucket_name, Key=obj["Key"])
        freed += obj["Size"]

def safe_upload_image(file_bytes: bytes, object_name: str, content_type: str = "image/jpeg") -> str:
    """Guards against exceeding 10 GB quota before executing upload."""
    bucket_name = os.getenv("R2_BUCKET_NAME")
    incoming_size = len(file_bytes)

    # 1. Reject individual files larger than 10 MB
    if incoming_size > 10 * 1024 * 1024:
        raise ValueError("File exceeds individual max limit of 10 MB.")

    # 2. Check total storage bucket size
    current_storage = get_bucket_total_size(bucket_name)

    # 3. If storage exceeds 8 GB safety buffer, auto-delete oldest images
    if current_storage + incoming_size > MAX_BUCKET_SIZE_BYTES:
        bytes_to_free = (current_storage + incoming_size) - MAX_BUCKET_SIZE_BYTES
        delete_oldest_objects(bucket_name, max(bytes_to_free, 500 * 1024 * 1024)) # Free at least 500 MB

    # 4. Upload file
    s3.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=file_bytes,
        ContentType=content_type
    )
    return f"https://pub-{os.getenv('R2_ACCOUNT_ID')}.r2.dev/{object_name}"