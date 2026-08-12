from sqlalchemy import select, func
from sqlalchemy.orm import Session
from datetime import datetime

from app.models import Backup, Failure, Restore

from app.aws_s3 import (
    generate_backup_content,
    upload_backup_to_s3,
    download_backup_from_s3
)

# =====================================================
# Backup Service
# =====================================================

def create_backup(db: Session):

    backup = Backup(
        status="SUCCESS"
    )

    db.add(backup)
    db.commit()
    db.refresh(backup)

    backup_name = f"backup-{backup.id:03}"

    content = generate_backup_content()

    s3_object_key = upload_backup_to_s3(
        content=content,
        backup_name=backup_name
    )

    backup.s3_object_key = s3_object_key

    db.commit()
    db.refresh(backup)

    return {
        "backup_id": backup.id,
        "status": backup.status,
        "created_at": backup.created_at,
        "storage": "AWS S3",
        "s3_object_key": backup.s3_object_key
    }


def get_backups(db: Session):

    backups = db.scalars(
        select(Backup)
    ).all()

    return {
        "total_backups": len(backups),
        "backups": backups
    }

from app.models import Failure

# =====================================================
# Failure Service
# =====================================================

def simulate_failure(db):

    failure = Failure(
        status="FAILED"
    )

    db.add(failure)
    db.commit()
    db.refresh(failure)

    return {
        "failure_id": failure.id,
        "status": failure.status,
        "failure_time": failure.failure_time
    }


def get_failures(db):

    failures = db.scalars(
        select(Failure)
    ).all()

    return {
        "total_failures": len(failures),
        "failures": failures
    }


from app.models import Restore

# =====================================================
# Restore Service
# =====================================================

def restore_system(db: Session):

    # =====================================================
    # Find the latest failure
    # =====================================================

    last_failure = db.scalar(
        select(Failure)
        .order_by(
            Failure.failure_time.desc()
        )
    )

    if last_failure is None:
        return {
            "error": "No failure has been simulated."
        }

    # =====================================================
    # Find the latest successful backup BEFORE the failure
    # =====================================================

    last_backup = db.scalar(
        select(Backup)
        .where(
            Backup.status == "SUCCESS",
            Backup.created_at <= last_failure.failure_time
        )
        .order_by(
            Backup.created_at.desc()
        )
    )

    if last_backup is None:
        return {
            "error": "No valid backup exists before the failure."
        }

    if not last_backup.s3_object_key:
        return {
            "error": "Selected backup is not stored in S3."
        }

    # =====================================================
    # Download backup from AWS S3
    # =====================================================

    try:

        backup_content = download_backup_from_s3(
            last_backup.s3_object_key
        )

    except Exception as e:

        return {
            "error": "Failed to download backup from S3.",
            "details": str(e)
        }

    # =====================================================
    # Validate backup
    # =====================================================

    if not backup_content:

        return {
            "error": "Downloaded backup is empty."
        }

    if "Cloud DR Backup" not in backup_content:

        return {
            "error": "Backup validation failed."
        }

    # =====================================================
    # Recovery completed
    # =====================================================

    recovery_time = datetime.now()

    # RTO = time from failure to successful recovery
    rto = (
        recovery_time - last_failure.failure_time
    ).total_seconds()

    # =====================================================
    # Save restore record
    # =====================================================

    restore = Restore(
        status="RECOVERED",
        recovery_time=recovery_time,
        rto_seconds=rto
    )

    db.add(restore)
    db.commit()
    db.refresh(restore)

    # =====================================================
    # Response
    # =====================================================

    return {
        "restore_id": restore.id,
        "status": restore.status,
        "recovery_time": restore.recovery_time,
        "rto_seconds": restore.rto_seconds,
        "source_backup_id": last_backup.id,
        "s3_object_key": last_backup.s3_object_key,
        "recovery": "S3 backup downloaded and validated successfully"
    }

# =====================================================
# Restore History
# =====================================================

def get_restores(db: Session):

    restores = db.scalars(
        select(Restore)
    ).all()

    return {
        "total_restores": len(restores),
        "restores": restores
    }


from sqlalchemy import func, select

# =====================================================
# Metrics Service
# =====================================================

def get_metrics(
    db: Session,
    app_name
):

    # =====================================================
    # Total Counts
    # =====================================================

    total_backups = db.scalar(
        select(func.count()).select_from(Backup)
    )

    total_failures = db.scalar(
        select(func.count()).select_from(Failure)
    )

    total_restores = db.scalar(
        select(func.count()).select_from(Restore)
    )

    # =====================================================
    # Latest Records
    # =====================================================

    last_backup = db.scalar(
        select(Backup)
        .order_by(
            Backup.created_at.desc()
        )
    )

    last_failure = db.scalar(
        select(Failure)
        .order_by(
            Failure.failure_time.desc()
        )
    )

    last_restore = db.scalar(
        select(Restore)
        .order_by(
            Restore.recovery_time.desc()
        )
    )

    # =====================================================
    # RPO Calculation
    # =====================================================

    rpo_seconds = None

    if last_failure is not None:

        # Find the latest successful backup
        # created before the failure
        backup_before_failure = db.scalar(
            select(Backup)
            .where(
                Backup.status == "SUCCESS",
                Backup.created_at <= last_failure.failure_time
            )
            .order_by(
                Backup.created_at.desc()
            )
        )

        if backup_before_failure is not None:

            rpo_seconds = (
                last_failure.failure_time
                - backup_before_failure.created_at
            ).total_seconds()

    # =====================================================
    # Metrics Response
    # =====================================================

    return {

        "application": app_name,

        "status": "healthy",

        "total_backups": total_backups,

        "total_failures": total_failures,

        "total_restores": total_restores,

        "rpo_seconds": rpo_seconds,

        "last_backup": last_backup,

        "last_failure": last_failure,

        "last_restore": last_restore

    }