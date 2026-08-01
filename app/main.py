import os
from typing import Generator

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, String, Integer, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

APP_NAME = os.getenv("APP_NAME", "Cloud DR Demo API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
AWS_REGION = os.getenv("AWS_REGION", "local")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cloud_dr.db")

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)


Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Demo API for a cloud-native multi-region disaster recovery project.",
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "region": AWS_REGION,
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "region": AWS_REGION}


@app.get("/status")
def status():
    return {
        "application": APP_NAME,
        "version": APP_VERSION,
        "region": AWS_REGION,
        "status": "healthy",
    }


@app.get("/users", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return db.scalars(select(User).order_by(User.id)).all()


@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == user.email))
    if existing:
        raise HTTPException(status_code=409, detail="A user with this email already exists.")

    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
