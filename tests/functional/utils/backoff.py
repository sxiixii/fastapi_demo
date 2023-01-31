import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
loggingStreamHandler = logging.StreamHandler()


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            n = 0
            while True:
                if func(*args, **kwargs):
                    break
                n += 1
                logger.info(f"Соединение не установлено. Пробуем подключиться снова. Выполнено {n} попыток")
                sleep_time = sleep_time * factor
                if sleep_time > border_sleep_time:
                    sleep_time = border_sleep_time
                time.sleep(sleep_time)
        return inner
    return func_wrapper
