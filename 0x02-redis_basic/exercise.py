#!/usr/bin/env python3
"""Writing strings to Redis
"""

import redis
import uuid
from typing import Union

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
