import inspect
import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from typing import List, Optional, Union, Type

from vigorish.app import Vigorish

from app.core.enums import RedisStatus, RedisEvent
from app.core.redis import redis
from app.core.config import settings

TIMESTAMP = "%m/%d/%Y %I:%M:%S %p"
IGNORE_KEY_TYPES = [Vigorish]


class cache:
    """Decorator that retrieves cached responses and stores uncached responses for an API endpoint."""

    def __init__(
        self,
        logger: Optional[logging.Logger] = None,
        ex: Optional[Union[int, timedelta]] = None,
        px: Optional[Union[int, timedelta]] = None,
        nx: Optional[bool] = False,
        xx: Optional[bool] = False,
        keepttl: Optional[bool] = False,
        ignore_key_types: Optional[List[Type[object]]] = IGNORE_KEY_TYPES,
    ):
        self.logger = logger
        self.ex = ex
        self.px = px
        self.nx = nx
        self.xx = xx
        self.keepttl = keepttl
        self.ignore_key_types = ignore_key_types

    def __call__(self, func):
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(func.__module__)
            self.logger.setLevel(logging.INFO)

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Return cached value if one exists, otherwise the value returned by the function is added to the cache."""
            if settings.REDIS_CLIENT_STATUS != RedisStatus.CONNECTED:
                return func(*args, **kwargs)
            key = get_cache_key(func, *args, **kwargs)
            in_cache = redis.get(key)
            if in_cache:
                write_to_log(RedisEvent.KEY_FOUND_IN_CACHE, key=key)
                return json.loads(in_cache)
            response = func(*args, **kwargs)
            if not redis.set(
                name=key,
                value=json.dumps(response),
                ex=self.ex,
                px=self.px,
                nx=self.px,
                xx=self.xx,
                keepttl=self.keepttl,
            ):
                write_to_log(RedisEvent.FAILED_TO_CACHE_KEY, key=key, value=response)
            else:
                write_to_log(RedisEvent.KEY_ADDED_TO_CACHE, key=key)
            return response

        def get_cache_key(func, *args, **kwargs):
            """Create a key that uniquely identifies the function and values of all arguments."""
            sig = inspect.signature(func)
            sig_params = sig.parameters
            args = sig.bind(*args, **kwargs)
            args.apply_defaults()
            args = args.arguments
            args_str = "_".join(f"{arg}={val}" for arg, val in args.items() if not ignore_arg_type(arg, sig_params))
            return f"{func.__name__}({args_str})"

        def ignore_arg_type(arg_name, sig_params):
            """Check if a function arg is of a type that must NOT be used to construct the cache key."""
            return any(sig_params[arg_name].annotation is ignore_type for ignore_type in self.ignore_key_types)

        def write_to_log(event: RedisEvent, key: str, value: Optional[str] = None):
            """Log `RedisEvent` details using the configured `Logger` object"""
            message = f"| {get_log_time()} | {event}: key={key}"
            if value:
                message += f", value={value}"
            self.logger.info(message)

        def get_log_time():
            """Get a timestamp to include with a log message."""
            return datetime.now().strftime(TIMESTAMP)

        return wrapper
