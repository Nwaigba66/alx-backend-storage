#!/usr/bin/env python3
"""Writing strings to Redis
"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps

types = [str, bytes, int, float]


def replay(method) -> None:
    """replay function to display the history of calls
    """
    self = method.__self__
    key = method.__qualname__
    input_key = f"{key}:inputs"
    output_key = f"{key}:outputs"
    input_history = self._redis.lrange(input_key, 0, -1)
    output_history = self._redis.lrange(output_key, 0, -1)
    print(f'Cache.store was called {int(self._redis.get(key))} times:')
    for this_key, value in zip(*(input_history, output_history)):
        print("Cache.store(*{}) -> {}".format(
            this_key.decode("utf-8"), value.decode('utf-8')))


def call_history(method: Callable) -> Callable:
    """A decorator to store the history of inputs and outputs
    """
    @wraps(method)
    def wrapper(self, *args):
        """Create keys for input and output list
        """
        key = method.__qualname__
        input_key = f"{key}:inputs"
        output_key = f"{key}:outputs"
        """Execute the wrapped function to retrieve the output
        """
        output = method(self, *args)
        self._redis.rpush(input_key, str(args))
        """Store the output using RPUSH in the "...:outputs" list
        """
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def count_calls(method: Callable) -> Callable:
    """Takes a single method Callable and returns a Callable
    Arguments:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function
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

    def get(self, key: str, fn: Callable = None) -> Callable:
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
