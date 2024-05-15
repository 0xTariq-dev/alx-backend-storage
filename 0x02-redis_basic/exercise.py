#!/usr/bin/env python3
"""This is a module for the exercise of the course."""

import redis
from uuid import uuid4 as uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """This decorator will count the number of calls to a function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        if isinstance(self, Cache):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """This class is for the exercise of the course."""
    def __init__(self):
        """Constructor for the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data in the database."""
        key = str(uuid())
        self._redis.set(key, data)
        return key

    def get(self,
            key: str,
            fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """Get the data from the database."""
        call = self._redis.get(key)
        return fn(call) if fn is not None else call

    def get_str(self, key: str) -> str:
        """Get the data from the database as a string."""
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Get the data from the database as an integer."""
        return self.get(key, lambda x: int(x))
