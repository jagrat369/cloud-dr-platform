from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import admin_required
from app.database import get_db
from app.services import restore_system, get_restores


router = APIRouter(
    prefix="/restore",
    tags=["Restore"]
)


# =====================================================
# Restore System
# =====================================================

@router.post("")
def restore(
    current_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    return restore_system(db)


# =====================================================
# Restore History
# =====================================================

@router.get("/history")
def restore_history(
    current_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    return get_restores(db)