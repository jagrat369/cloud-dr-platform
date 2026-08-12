from pydantic import BaseModel, EmailStr, Field


# ======================================================
# User Registration
# ======================================================

class UserCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=100
    )


# ======================================================
# User Login
# ======================================================

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# ======================================================
# User Response
# ======================================================

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


# ======================================================
# JWT Token
# ======================================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None