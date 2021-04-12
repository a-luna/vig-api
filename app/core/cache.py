import inspect
import json
import logging
from datetime import datetime
from functools import wraps

from vigorish.util.dt_format_strings import DT_NAIVE

from app.core.redis import get_cached_response, cache_response

IGNORE_ARGS = ["app"]


class cache:
    """Decorator that retrieves cached responses and stores uncached responses for an API endpoint."""

    def __init__(self, logger=None, ignore_args=IGNORE_ARGS):
        self.logger = logger
        self.ignore_args = ignore_args

    def __call__(self, func):
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(func.__module__)
            self.logger.setLevel(logging.INFO)

        @wraps(func)
        def wrapper(*args, **kwargs):
            exec_start_str = datetime.now().strftime(DT_NAIVE)
            key = convert_func_sig_to_key(func, *args, **kwargs)
            cached_data = get_cached_response(key)
            if cached_data:
                self.logger.info(f"{exec_start_str} | FOUND IN CACHE: key={key}")
                return json.loads(cached_data)
            response = func(*args, **kwargs)
            cache_data = json.dumps(response)
            if not cache_response(key, cache_data):
                self.logger.info(f"{exec_start_str} |   CACHE FAILED: key={key}, value={cache_data}")
            else:
                self.logger.info(f"{exec_start_str} | ADDED TO CACHE: key={key}")
            return response

        def convert_func_sig_to_key(func, *args, **kwargs):
            """Return a string containing function name and list of all argument names/values."""
            args = inspect.signature(func).bind(*args, **kwargs)
            args.apply_defaults()
            args_str = "_".join(f"{arg}={val}" for arg, val in args.arguments.items() if arg_is_not_ignored(arg))
            return f"{func.__name__}-{args_str}"

        def arg_is_not_ignored(arg_name):
            return all(arg_name not in restricted for restricted in self.ignore_args)

        return wrapper
