import logging
import sys
from typing import Tuple

from loguru import logger
from starlette.config import Config

from app.core.logging import InterceptHandler

config = Config(".env")

# API Prefix
API_PREFIX: str  = config("API_PREFIX", default="/api/v1")

# API Version
VERSION: str = config("VERSION", default="1.0.0") 

# Application Settings
DEBUG: bool = config("DEBUG", cast=bool, default=False)
PROJECT_NAME: str = config("PROJECT_NAME", default="Media Server API")

# Ant Server
ANT_HOST: str = config("ANT_HOST", default="localhost")
ANT_PORT: str = config("ANT_PORT", default="5080")
ANT_REST_PATH: str = config("ANT_REST_PATH", default="WebRTCApp/rest/v2")

# Database
DB_USER: str = config("DB_USER", default="root")
DB_PASSWORD: str = config("DB_PASSWORD", default="admin")
DB_HOST: str = config("DB_HOST", default="localhost")
DB_PORT: str = config("DB_PORT", default="27017")
DB_NAME: str = config("DB_NAME", default="backup_db")

# Logging Settings 

LOGGING_LEVEL: int = logging.DEBUG if DEBUG else logging.INFO
LOGGERS: Tuple[str, str] =  ("uvicorn.asgi", "uvicorn.acces")

logging.getLogger().handlers = [InterceptHandler()]

for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])