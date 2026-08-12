from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import APP_NAME
from app.database import get_db
from app.services import get_metrics

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)


@router.get("")
def metrics(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_metrics(
        db=db,
        app_name=APP_NAME
    )