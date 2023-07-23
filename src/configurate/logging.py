import logging

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname:10} {pathname}:{lineno} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", ],
            "level": "DEBUG",
            "propagate": False,
        }
    }
}
import logging.config
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("")

logger.debug("HHh")
