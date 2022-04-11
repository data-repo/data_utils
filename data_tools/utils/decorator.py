
import time
from functools import wraps
from data_tools.utils.logger import Logger


def retry(exception_check: Exception or tuple,
          tries: int = 4,
          delay: float = 3.0,
          backoff: int = 2,
          logger: Logger = None):
    """
    Retry calling the decorated function using an exponential backoff
    Args:
        exception_check: the exception to check. may be a tuple of exceptions to check
        tries: number of times to try (not retry) before giving up
        delay: initial delay between retries in seconds
        backoff: backoff multiplier e.g. value of 2 will double the delay each retry
        logger: logger to use. If None, print
    Returns:
    """
    def decorator_retry(func):
        @wraps(func)
        def function_retry(*args, **kwargs):
            tries_counter, delay_counter = tries, delay
            while tries_counter > 1:
                try:
                    return func(*args, **kwargs)
                except exception_check as e:
                    msg = f'{e}, Retrying in {delay_counter} seconds.'
                    if logger:
                        logger.warning(msg=msg, func=func)
                    else:
                        print(msg)
                    time.sleep(delay_counter)
                    tries_counter -= 1
                    delay_counter *= backoff
            return func(*args, **kwargs)
        return function_retry
    return decorator_retry


def timer(threshold_time: int = 2000,
          logger: Logger = None):
    """
    Calculate time for running functions
    Args:
        threshold_time: Waiting for function runtime in milliseconds
        logger: logger to use. If None, print
    Returns:
    """
    def decorator_timer(func):
        @wraps(func)
        def function_timer(*args, **kwargs):
            start_time = time.perf_counter()
            ret = func(*args, **kwargs)
            stop_time = time.perf_counter()
            duration = round((stop_time - start_time) * 1000, 3)
            if duration > threshold_time:
                msg = f'Running time is out of threshold (threshold: {threshold_time} ms, duration: {duration} ms)'
                if logger:
                    logger.warning(msg=msg, func=func)
                else:
                    print(msg)
            else:
                msg = f'Running time is: {duration} ms'
                if logger:
                    logger.info(msg=msg, func=func)
                else:
                    print(msg)
            return ret
        return function_timer
    return decorator_timer
