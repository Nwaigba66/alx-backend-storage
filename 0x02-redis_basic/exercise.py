#!/usr/bin/env python3
"""Writing strings to Redis
"""

import redis
import uuid
from typing import Union, Callable

types = [str, bytes, int, float]


class Cache:
    def __init__(self):
        """Initialize redis client
        """
        self._redis = redis.Redis()

        """Flush the redis database
        """
        self._redis.flushdb()

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
