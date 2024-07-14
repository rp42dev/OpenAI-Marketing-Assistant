from functools import wraps
from openai import APIError, APIConnectionError, RateLimitError


def _handle_api_exceptions(func):
    """Decorator to handle common API exceptions."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except (APIError, APIConnectionError, RateLimitError) as e:
            return f"An error occurred in the \"{func.__name__}\" function: {e}"
    return wrapper
