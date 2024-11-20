from pydantic import BaseModel
from logging.config import dictConfig
import logging
from datetime import datetime

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "mycoolapp"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file_log": {
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": f'./logs/{datetime.now().strftime("%d-%m-%Y_%H:%M:%S")}.log',
        }

    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["default", "file_log"], "level": LOG_LEVEL},
    }

dictConfig(LogConfig().dict())
logger = logging.getLogger("mycoolapp")

