from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.auth_service import register_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return db.scalars(
        select(User).order_by(User.id)
    ).all()


@router.post(
    "",
    response_model=UserResponse,
    status_code=201
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.scalar(
        select(User).where(
            User.email == user.email
        )
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists."
        )

    new_user = register_user(
        db=db,
        name=user.name,
        email=user.email,
        password=user.password
    )

    if new_user is None:
        raise HTTPException(
            status_code=409,
            detail="A user with this email already exists."
        )

    return new_user
