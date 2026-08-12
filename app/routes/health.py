from fastapi import APIRouter

from app.config import APP_NAME, APP_VERSION, AWS_REGION

router = APIRouter(tags=["Health"])


@router.get("/")
def root():

    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "region": AWS_REGION,
        "status": "running"
    }


@router.get("/health")
def health():

    return {
        "status": "healthy",
        "region": AWS_REGION
    }


@router.get("/status")
def status():

    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "region": AWS_REGION,
        "status": "healthy"
    }