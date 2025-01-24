import logging
import sys
from typing import Dict, Any

from loguru import logger

LOG_FORMAT = '{time:YYYY-MM-DD HH:mm:ss} [{level}] {module}:{name}:{line} - {message}'

logger.add("logs/info.log", filter=lambda record: "INFO" in record['level'].name, rotation="10 MB",
           retention="3 days", level="INFO", format=LOG_FORMAT)
logger.add("logs/trace.log", filter=lambda record: "TRACE" in record['level'].name, level="TRACE")
logger.add("logs/debug.log", filter=lambda record: "DEBUG" in record['level'].name, rotation="10 MB",
           retention="3 days", level="DEBUG", format=LOG_FORMAT)
logger.add("logs/warning.log", filter=lambda record: "WARNING" in record['level'].name, rotation="10 MB",
          retention="3 days", level="WARNING", format=LOG_FORMAT)
logger.add("logs/error.log", filter=lambda record: "ERROR" in record['level'].name, rotation="10 MB",
           retention="1 days", level="ERROR", format=LOG_FORMAT)


S_LOGGING_CONFIG_DEFAULTS: Dict[str, Any] = dict(  # no cov
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sanic.root": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": False,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": False,
            "qualname": "sanic.access",
        },
        "sanic.server": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
            "qualname": "sanic.server",
        },
    },
    handlers={
        "console": {
            "class": "logger.InterceptHandler",
        },
        "error_console": {
            "class": "logger.InterceptHandler",
        },
        "access_console": {
            "class": "logger.InterceptHandler",
        },
    }
)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno
        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_log(level: str = "INFO"):
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(level)
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": False}])