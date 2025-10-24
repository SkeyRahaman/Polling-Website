from logging.handlers import RotatingFileHandler
import structlog
import logging
import os
import sys

from django.conf import settings

os.makedirs(settings.LOG_FOLDERNAME, exist_ok=True)

rotating_handler = RotatingFileHandler(
    f"{settings.LOG_FOLDERNAME}/{settings.LOG_FILENAME}",
    maxBytes=settings.LOG_MAX_BYTES,
    backupCount=settings.LOG_BACKUP_COUNT,
)

# Configure logging
logging.basicConfig(
    format="\n%(message)s",
    level=logging._nameToLevel.get(settings.LOG_LEVEL, logging.INFO),
    handlers=[
        rotating_handler,
        logging.StreamHandler(sys.stdout)
    ],
)

# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.CallsiteParameterAdder(
            parameters=[
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.FUNC_NAME,
            ]
        ),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

def get_logger(name: str = __name__)-> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
