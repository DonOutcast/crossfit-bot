# import json
# import logging
# import functools
# import logging.config

# from configurate.config import CONFIGURATE_DIR, LOGGING
from configurate.config import LOGGING

class LoggerCore:

    def __init__(self, path_to_file: str):
        self.path = path_to_file
        self._set_configurate()

    def _set_configurate(self) -> None:
        logging.config.dictConfig(LOGGING)


def get_my_logger(name: str) -> logging:
    return logging.getLogger(name)


def debugorator(debug_on: bool):
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(*args, **kwargs):
            result = None
            try:
                result = await function(*args, **kwargs)
            except Exception as ex:
                logger_exception = get_my_logger("logger_exception")
                logger_exception.exception(f"User id: {args[0].from_user.id}")
            logger_debug = get_my_logger("logger_info")
            logger_debug.info(
                f"Function: {function.__name__}. User id: {args[0].from_user.id}. User name {args[0].from_user.full_name}."
            )
            if debug_on:
                logger_debug = get_my_logger("logger_debug")
                logger_debug.debug(
                    f"Function: {function.__name__}. User id: {args[0].from_user.id}. User name {args[0].from_user.full_name}."
                )
            return result

        return wrapper

    return decorator


def databasorator(debug_on: bool):
    def decorator(function):
        @functools.wraps(function)
        async def wrapper(*args, **kwargs):
            result = None
            try:
                result = await function(*args, **kwargs)
            except Exception as ex:
                logger_exception = get_my_logger("logger_exception")
                logger_exception.exception(f"User id: {args[0].from_user.id}")
            logger_debug = get_my_logger("logger_info")
            logger_debug.info(
                f"Function: {function.__name__}. User id: {args[0].from_user.id}. User name {args[0].from_user.full_name}."
            )
            if debug_on:
                logger_debug = get_my_logger("logger_debug")
                logger_debug.debug(
                    f"Function: {function.__name__}. User id: {args[0].from_user.id}. User name {args[0].from_user.full_name}."
                )
            return result

        return wrapper

    return decorator


# logger = LoggerCore(CONFIGURATE_DIR)
