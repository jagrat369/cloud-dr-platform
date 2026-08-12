from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import create_access_token, get_current_user
from app.auth_service import (
    authenticate_user,
    get_user_by_email,
    register_user,
)
from app.database import get_db
from app.schemas import (
    Token,
    UserCreate,
    UserResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# =====================================================
# Register
# =====================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = register_user(
        db=db,
        name=user.name,
        email=user.email,
        password=user.password
    )

    if new_user is None:
        raise HTTPException(
            status_code=409,
            detail="User already exists."
        )

    return new_user


# =====================================================
# Login
# =====================================================

@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    authenticated_user = authenticate_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )

    if authenticated_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    access_token = create_access_token(
        data={
            "sub": authenticated_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# =====================================================
# Current Logged-in User
# =====================================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(
        db=db,
        email=current_user
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )
    return user