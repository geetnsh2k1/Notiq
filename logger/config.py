import logging
from logging.config import dictConfig

from config.client import ConfigClient

log_level = ConfigClient.get_property("LOG_LEVEL")
log_format = ConfigClient.get_property("LOG_FORMAT")

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(name)s: %(message)s"
        },
        "json": {
            "format": (
                '{"time": "%(asctime)s", "level": "%(levelname)s", '
                '"name": "%(name)s", "message": "%(message)s"}'
            )
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": log_format,
        },
    },
    "root": {
        "level": log_level,
        "handlers": ["console"],
    },
    "loggers": {
        "my_app": {"level": log_level, "handlers": ["console"], "propagate": False},
    },
}


def setup_logging():
    dictConfig(LOGGING_CONFIG)
