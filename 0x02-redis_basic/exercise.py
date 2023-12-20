#!/usr/bin/env python3
"""Writing strings to Redis
"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps

types = [str, bytes, int, float]


def call_history(method: Callable) -> Callable:
    """A decorator to store the history of inputs and outputs for a particular function
    """
    @wraps(method)
    def wrapper(self, *args):
        """Initialize redis client
        """
        self._redis = redis.Redis()

        """Create keys for input and output list
        """
        key = method.__qualname__
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        """Execute the wrapped function to retrieve the output
        """
        output = method(self, *args)

        self._redis.rpush(input_key, str(args))
        """Store the output using RPUSH in the "...:outputs" list
        """
        self._redis.rpush(output_key, str(args))
        return output
    return wrapper    


def count_calls(method: Callable) -> Callable:
        """Takes a single method Callable and returns a Callable
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
                key = method.__qualname__
                self._redis.incr(key)
                return method(self, *args, **kwargs)
        return wrapper


class Cache:
    def __init__(self):
        """Initialize redis client
        """
        self._redis = redis.Redis()

        """Flush the redis database
        """
        self._redis.flushdb()

    
    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Generate a random key using uuid
        """
        key = str(uuid.uuid4())

        """Store the input data in redis using the random key
        """
        self._redis.set(key, data)
        """Return the key
        """
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, None]:
        """Get the data in a given key location
        """
        data = self._redis.get(key)
        if data is not None:
            if fn:
                return fn(data)
            return data
        return None

    def get_str(self, Callable) -> Union[str, None]:
        """Returns a Callable to convert to string
        """
        return lambda d: d.decode("utf-8")

    def get_int(self, Callable) -> Union[int, None]:
        """Returns a Callable to convert to integer
        """
        return int
