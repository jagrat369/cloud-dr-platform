from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import hash_password, verify_password
from app.models import User


# ==============================
# Register User
# ==============================

def register_user(
    db: Session,
    name: str,
    email: str,
    password: str
):

    existing = db.scalar(
        select(User).where(User.email == email)
    )

    if existing:
        return None

    user = User(
        name=name,
        email=email,
        hashed_password=hash_password(password),
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# ==============================
# Authenticate User
# ==============================

def authenticate_user(
    db: Session,
    email: str,
    password: str
):

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user


# ==============================
# Get User by Email
# ==============================

def get_user_by_email(
    db: Session,
    email: str
):

    return db.scalar(
        select(User).where(User.email == email)
    )


# ==============================
# Check Admin Role
# ==============================

def is_admin(
    db: Session,
    email: str
):

    user = get_user_by_email(
        db=db,
        email=email
    )

    if user is None:
        return False

    return user.role == "admin"