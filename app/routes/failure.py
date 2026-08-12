from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import admin_required
from app.database import get_db
from app.services import simulate_failure, get_failures

router = APIRouter(
    prefix="/failure",
    tags=["Failure"]
)


@router.post("")
def failure(
    current_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    return simulate_failure(db)


@router.get("/history")
def failure_history(
    current_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    return get_failures(db)