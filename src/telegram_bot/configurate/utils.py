import os
import logging


def os_getenv(key: str, default=None) -> str:
    env_value = os.getenv(key, default)
    if env_value == '':
        logging.warning(
            f"ENV variable: {key} is set to empty string. Using default value instead ({default})"
        )
        env_value = default
    return env_value
