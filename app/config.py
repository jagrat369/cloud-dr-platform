import os

from dotenv import load_dotenv


# =====================================================
# Load environment variables
# =====================================================

load_dotenv()


# =====================================================
# Application
# =====================================================

APP_NAME = os.getenv(
    "APP_NAME",
    "Cloud DR Demo API"
)

APP_VERSION = os.getenv(
    "APP_VERSION",
    "2.0.0"
)


# =====================================================
# AWS
# =====================================================

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-south-1"
)

AWS_S3_BUCKET = os.getenv(
    "AWS_S3_BUCKET",
    "cloud-dr-platform-backups-2026"
)


# =====================================================
# Database
# =====================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./cloud_dr.db"
)