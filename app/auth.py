import os
from datetime import datetime, timedelta, UTC

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db

load_dotenv()

# ==============================
# JWT Configuration
# ==============================

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)

# ==============================
# OAuth2
# ==============================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# ==============================
# Password Hashing
# ==============================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# ==============================
# JWT Token Creation
# ==============================

def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ==============================
# JWT Verification
# ==============================

def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:
            return None

        return email

    except JWTError:
        return None


# ==============================
# Current User
# ==============================

def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    email = verify_token(token)

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    return email


# ==============================
# Admin Only
# ==============================

def admin_required(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    # Import here to avoid circular import
    from app.auth_service import get_user_by_email

    email = verify_token(token)

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    user = get_user_by_email(
        db=db,
        email=email
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required."
        )

    return user