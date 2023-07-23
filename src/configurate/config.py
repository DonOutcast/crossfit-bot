import os
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Any, Dict
from pydantic import BaseSettings, validator, SecretStr, RedisDsn, PostgresDsn, Field

from .utils import os_getenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "")


BASE_DIR = Path(__file__).absolute().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"
DATABASE_DIR = BASE_DIR / "databases/database.db"


class Settings(BaseSettings):
    bot_token: SecretStr
    bot_name: str
    admins: list[int]

    openweather_token: SecretStr

    container_name: str = Field(..., env="BOT_CONTAINER_NAME")
    image: str = Field(..., env="BOT_IMAGE_NAME")

    fsm_mode: str

    redis_user: str = Field(..., env="REDIS_DATABASE_USER")
    redis_pass: str = Field(..., env="REDIS_DATABASE_PASSWORD")
    redis_host: str = Field(..., env="REDIS_DATABASE_HOST")
    redis_port: str = Field(..., env="REDIS_DATABASE_PORT")
    redis_lvl: int = Field(..., env="REDIS_DATABASE_LEVEL")
    redis_dsn: RedisDsn

    database_mode: str
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_pass: str = Field(..., env="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., env="POSTGRES_DB_NAME")
    postgres_host: str = Field(..., env="POSTGRES_HOST")
    postgres_port: str = Field(..., env="POSTGRES_PORT")
    postgres_dsn: Optional[PostgresDsn]

    debug: bool

    @validator("fsm_mode")
    def check_fsm_mode(cls, value):
        if value not in ("memory", "redis"):
            raise ValueError("Incorrect fsm_mode. Must be one of: memory, redis")

    @validator("redis_dsn")
    def skip_validating_redis(cls, value, values):
        if values.get("fsm_mode") == "redis" and value is None:
            raise ValueError("Redis config is missing, though fsm_type is 'redis'")
        return value

    @validator("database_mode")
    def check_database_mode(cls, value):
        if value not in ("sqlite3", "postgresql"):
            raise ValueError("Incorrect database_mode. Must be one of: sqlite3, postgresql")
        return value

    @validator("postgres_dsn")
    def skip_validating_postgres(cls, value, values):
        if values.get("database_mode") == "postgresql" and value is None:
            raise ValueError("PostgreSql config is missing, though database_type is 'postgresql'")
        return value

    @validator("admins")
    def check_correct_admins_ids(cls, value):
        for i in value:
            if i < 0:
                raise ValueError("Incorrect admins ids. Must be only positive numbers.")
        return value

    class Config:
        env_file = '../../.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

LOGGING = {
    "version": 1,
    "formatters": {
        "debug_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s  - %(message)s - %(filename)s - %(module)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "info_formatter": {
            "format": "%(asctime)s - %(name)s - %(levelname)s  - %(message)s - %(filename)s - %(module)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "exception_formatter": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "debug_handler": {
            "class": "logging.StreamHandler",
            "formatter": "debug_formatter"
        },
        "info_handler": {
            # "class": "logging.handlers.RotatingFileHandler",
            # "mode": "a",
            # "filename": "log/logs.log",
            # "encoding": "UTF-8",
            # "maxBytes": 20,
            # "backupCount": 5,
            # "formatter": "main_formatter",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "log/file_log.log",
            "encoding": "UTF-8",
            "when": "D",
            "interval": 1,
            "backupCount": 365,
            "formatter": "info_formatter",
        },
        "exception_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "log/errors_log.log",
            "encoding": "UTF-8",
            "when": 'D',
            "interval": 1,
            "backupCount": 365,
            "formatter": "exception_formatter",
        }
    },
    "loggers": {
        "logger_debug": {
            "handlers": [
                "debug_handler"
            ],
            "propagate": True,
            "level": "DEBUG"
        },
        "logger_info": {
            "handlers": [
                "info_handler"
            ],
            "propagate": True,
            "level": "INFO",
        },
        "logger_exception": {
            "handlers": [
                "exception_handler",
            ],
            "propagate": True,
            "level": "ERROR",
        }
    }
}


