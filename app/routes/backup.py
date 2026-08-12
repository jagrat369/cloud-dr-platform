from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import admin_required
from app.database import get_db
from app.services import create_backup, get_backups

router = APIRouter(
    prefix="/backup",
    tags=["Backup"]
)


@router.post("")
def backup(
    current_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    return create_backup(db)


@router.get("/history")
def backup_history(
    current_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    return get_backups(db)