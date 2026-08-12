from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# =====================================================
# User Model
# =====================================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    role: Mapped[str] = mapped_column(
        String(20),
        default="user",
        nullable=False
    )


# =====================================================
# Backup Model
# =====================================================

class Backup(Base):
    __tablename__ = "backups"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    s3_object_key: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )


# =====================================================
# Failure Model
# =====================================================

class Failure(Base):
    __tablename__ = "failures"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    failure_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


# =====================================================
# Restore Model
# =====================================================

class Restore(Base):
    __tablename__ = "restores"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    recovery_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    rto_seconds: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )