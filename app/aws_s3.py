from datetime import datetime

import boto3
from botocore.exceptions import ClientError

from app.config import AWS_REGION, AWS_S3_BUCKET


# =====================================================
# AWS S3 Client
# =====================================================

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION
)


# =====================================================
# Generate Backup Content
# =====================================================

def generate_backup_content() -> str:

    return (
        "Cloud DR Backup\n"
        f"Generated At: {datetime.now().isoformat()}\n"
        "Status: SUCCESS\n"
    )


# =====================================================
# Upload Backup to S3
# =====================================================

def upload_backup_to_s3(
    content: str,
    backup_name: str
) -> str:

    object_key = f"backups/{backup_name}.txt"

    try:

        s3_client.put_object(
            Bucket=AWS_S3_BUCKET,
            Key=object_key,
            Body=content.encode("utf-8"),
            ContentType="text/plain"
        )

        return object_key

    except ClientError as e:

        raise RuntimeError(
            f"S3 upload failed: {e}"
        )


# =====================================================
# Download Backup from S3
# =====================================================

def download_backup_from_s3(
    object_key: str
) -> str:

    try:

        response = s3_client.get_object(
            Bucket=AWS_S3_BUCKET,
            Key=object_key
        )

        content = response["Body"].read().decode("utf-8")

        return content

    except ClientError as e:

        raise RuntimeError(
            f"S3 download failed: {e}"
        )