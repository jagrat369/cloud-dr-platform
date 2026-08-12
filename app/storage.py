"""
Temporary in-memory storage.

In production:
- Backups will be stored in Amazon S3
- Metadata will be stored in PostgreSQL
"""

backups = []

failures = []

restores = []