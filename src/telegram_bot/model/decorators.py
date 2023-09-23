import functools
from typing import Callable



def pre(condition: Callable, message: str):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            assert condition(*args, **kwargs), message
            result = func(*args, **kwargs)
            return result

        return inner

    return wrapper


def post(condition: Callable, message: str):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            assert condition(*args, **kwargs), message
            return result

        return inner

    return wrapper


# @pre(lambda x: x >= 0, "negative")
# @decorator("Hello world")
# def checked_log(x):
#     return x
