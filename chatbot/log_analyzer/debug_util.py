"""
Debugging decorator for synchronous and asynchronous functions.

Features:
- Takes a function and returns a wrapped version (usable as @debug_log or debug_log(func)).
- Logs function name and arguments before execution.
- Times execution using time.perf_counter().
- Logs execution time and return value after completion.
- Handles both synchronous and asynchronous functions.
- Catches exceptions, logs them, and re-raises.
- Uses the logging module for output.
- Includes example usage with regular and async functions.
- Uses modern Python (3.8+) features: decorators, asyncio, type hints, etc.
- Follows PEP 8 naming conventions and includes docstrings.
"""

import asyncio
import functools
import logging
import time
from typing import Any, Callable, Optional

def _get_logger(logger: Optional[logging.Logger]) -> logging.Logger:
    """Return the provided logger or a default one configured for the module."""
    if logger is not None:
        return logger
    log = logging.getLogger(__name__)
    if not log.handlers:
        # Minimal basic configuration if no handlers exist
        logging.basicConfig(level=logging.INFO)
    return log


def debug_log(
    _func: Optional[Callable[..., Any]] = None,
    *,
    logger: Optional[logging.Logger] = None,
    level: int = logging.INFO,
) -> Callable[..., Any]:
    """
    Decorator that logs function calls, times execution, and logs results.

    Can be used with or without parentheses:
        @debug_log
        def foo(...): ...

        @debug_log(logger=my_logger, level=logging.DEBUG)
        def bar(...): ...

    Parameters:
        _func: The function to wrap (used when the decorator is applied directly).
        logger: Optional logger to emit logs to. If None, a default logger is created.
        level: Logging level to use (default INFO).

    Returns:
        A wrapped function (sync or async) with the same signature as the input.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        log = _get_logger(logger)

        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                log.log(level, f"Calling {func.__qualname__} with args={args}, kwargs={kwargs}")
                start = time.perf_counter()
                try:
                    result = await func(*args, **kwargs)
                except Exception as exc:
                    elapsed = time.perf_counter() - start
                    log.exception(
                        f"Exception in {func.__qualname__} after {elapsed:.6f}s: {exc}"
                    )
                    raise
                else:
                    elapsed = time.perf_counter() - start
                    log.log(level, f"{func.__qualname__} returned {result!r} in {elapsed:.6f}s")
                    return result

            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                log.log(level, f"Calling {func.__qualname__} with args={args}, kwargs={kwargs}")
                start = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                except Exception as exc:
                    elapsed = time.perf_counter() - start
                    log.exception(
                        f"Exception in {func.__qualname__} after {elapsed:.6f}s: {exc}"
                    )
                    raise
                else:
                    elapsed = time.perf_counter() - start
                    log.log(level, f"{func.__qualname__} returned {result!r} in {elapsed:.6f}s")
                    return result

            return sync_wrapper

    if _func is None:
        return decorator
    else:
        return decorator(_func)


# Example usage
if __name__ == "__main__":
    # Basic logging configuration for the example
    logging.basicConfig(level=logging.INFO)

    @debug_log
    def add(a: int, b: int) -> int:
        """
            Simple synchronous function to add two numbers.
        """
        return a + b

    @debug_log
    async def async_multiply(a: int, b: int) -> int:
        """
            Asynchronous function that multiplies two numbers after a brief await.
        """
        await asyncio.sleep(0.01)
        return a * b

    @debug_log
    def faulty_divide(a: int, b: int) -> float:
        """
            Function designed to raise an exception for demonstration.
        """
        return a / b

    async def run_async_examples():
        result = await async_multiply(6, 7)
        print(f"Async result: {result}")

    # Run synchronous example
    print(f"Sync add(3, 4) = {add(3, 4)}")

    # Run asynchronous example
    asyncio.run(run_async_examples())

    # Run function that raises an exception to demonstrate logging and re-raise
    try:
        faulty_divide(10, 0)
    except ZeroDivisionError:
        pass  # Exception is logged by the decorator