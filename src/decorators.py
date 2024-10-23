import functools
from loguru import logger
from data.settings import MAX_RETRIES
from traceback import format_exc
from src.utils import random_sleep


def retry(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for _ in range(MAX_RETRIES):
            try:
                res = func(*args, **kwargs)
                return res
            except Exception as e:
                logger.warning(
                    f"{func.__name__} - Traceback - {format_exc()}, exception: {repr(e)}"
                )
                random_sleep()
        else:
            return None

    return wrapper
