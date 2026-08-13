# Create a prompt that generates a Python decorator utility capable of wrapping 
# any function to provide execution insights.

# Your generated solution should:

#     Take any function and wrap it to log execution details
#     Time the function execution using time.perf_counter() or time.time()
#     Log the function name and input arguments before execution
#     Log the return value after execution
#     Catch and log any exceptions that occur
#     Return the result (or re-raise the error with proper logging)
#     Use the logging module or print statements
#     Support both synchronous and asynchronous functions
#     Use modern Python features (decorators, *args, **kwargs, asyncio)

# Here's a Python decorator that wraps any function (sync or async) to log execution details, time the call, log inputs/outputs, and log exceptions. It uses the logging module and supports both synchronous and asynchronous functions via asyncio.

import asyncio
import inspect
import time
import logging
import functools

def log_execution(
    _func=None,
    *,
    logger=None,
    level=logging.INFO,
    log_args=True,
    log_kwargs=True,
    log_return=True,
    log_exceptions=True
):
    # Configure a default logger if none provided
    if logger is None:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logging.basicConfig(level=logging.INFO)

    def _wrap_sync(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            if log_args or log_kwargs:
                if log_args and log_kwargs:
                    logger.log(level, f"Calling {fn.__qualname__} with args={args}, kwargs={kwargs}")
                elif log_args:
                    logger.log(level, f"Calling {fn.__qualname__} with args={args}")
                else:
                    logger.log(level, f"Calling {fn.__qualname__} with kwargs={kwargs}")

            start = time.perf_counter()
            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                elapsed = time.perf_counter() - start
                if log_exceptions:
                    logger.exception(
                        f"Exception in {fn.__qualname__} after {elapsed:.6f}s: {exc}"
                    )
                raise
            else:
                elapsed = time.perf_counter() - start
                if log_return:
                    logger.log(level, f"{fn.__qualname__} returned {result!r} in {elapsed:.6f}s")
                return result
        return wrapper

    def _wrap_async(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            if log_args or log_kwargs:
                if log_args and log_kwargs:
                    logger.log(level, f"Calling {fn.__qualname__} with args={args}, kwargs={kwargs}")
                elif log_args:
                    logger.log(level, f"Calling {fn.__qualname__} with args={args}")
                else:
                    logger.log(level, f"Calling {fn.__qualname__} with kwargs={kwargs}")

            start = time.perf_counter()
            try:
                result = await fn(*args, **kwargs)
            except Exception as exc:
                elapsed = time.perf_counter() - start
                if log_exceptions:
                    logger.exception(
                        f"Exception in {fn.__qualname__} after {elapsed:.6f}s: {exc}"
                    )
                raise
            else:
                elapsed = time.perf_counter() - start
                if log_return:
                    logger.log(level, f"{fn.__qualname__} returned {result!r} in {elapsed:.6f}s")
                return result
        return wrapper

    # Support usage both with and without parentheses:
    if _func is None:
        return lambda f: log_execution(
            f,
            logger=logger,
            level=level,
            log_args=log_args,
            log_kwargs=log_kwargs if 'log_kwargs' in locals() else True,
            log_return=log_return,
            log_exceptions=log_exceptions
        )
    else:
        if asyncio.iscoroutinefunction(_func) or inspect.isasyncgenfunction(_func):
            return _wrap_async(_func)
        else:
            return _wrap_sync(_func)

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    @log_execution
    def add(a, b):
        return a + b

    @log_execution
    async def add_async(a, b):
        await asyncio.sleep(0.1)
        return a + b

    # Sync function usage
    print("Result:", add(2, 3))

    # Async function usage
    asyncio.run(add_async(4, 5))

# Notes:

#     Logs function name, input args/kwargs, timing, and return value.
#     Logs exceptions with a traceback via logger.exception and re-raises.
#     Works for methods, functions, and async functions.
#     Uses time.perf_counter() for high-resolution timing.
