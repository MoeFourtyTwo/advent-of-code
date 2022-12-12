import functools
import time
from typing import Callable

from loguru import logger


def timeit(f: Callable[[...], ...]):
    @functools.wraps(f)
    def timeit_wrapper(*args, **kwargs) -> Callable[[...], ...]:
        start_time = time.perf_counter()
        result = f(*args, **kwargs)
        end_time = time.perf_counter()
        logger.info(f"{f.__module__}.{f.__qualname__} took {end_time - start_time :.4f}s.")
        return result

    return timeit_wrapper
