from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "",
    response_model=list[UserResponse]
)
def get_users(db: Session = Depends(get_db)):

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

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user