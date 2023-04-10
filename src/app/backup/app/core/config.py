import os
import sys


def load_settings() -> None:
    if not os.environ.get("DB_USER"):
        check_settings("DB_USER", "root")
    
    if not os.environ.get("DB_PASSWORD"):
        check_settings("DB_PASSWORD", "admin")
    
    if not os.environ.get("DB_HOST"):
        check_settings("DB_HOST", "localhost")
    
    if not os.environ.get("DB_PORT"):
        check_settings("DB_PORT", "27017")

    if not os.environ.get("DB_NAME"):
        check_settings("DB_NAME", "backup_db")

    if not os.environ.get("ACTOR_WAIT_TIME"):
        check_settings("ACTOR_WAIT_TIME", 2.5)
    
    if not os.environ.get("ACTOR_WATCH_DIR"):
        check_settings("ACTOR_WATCH_DIR", "/streams")

    if not os.environ.get("S3_KEY_ID"):
        sys.exit("S3_KEY_ID must be set, this cannot be given a default value due to security issues.")

    if not os.environ.get("S3_SECRET_KEY"):
        sys.exit("S3_SECRET_KEY must be set, this cannot be given a default value due to security issues.")


def check_settings(var: str, val: str) -> None:
    if not os.environ.get(var):
        os.environ.update({var: val})
