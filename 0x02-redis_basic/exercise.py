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


def call_history(method: Callable) -> Callable:
    """This decorator will store the history of inputs and outputs."""
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        inputs = f'{method.__qualname__}:inputs'
        outputs = f'{method.__qualname__}:outputs'
        if isinstance(self, Cache):
            self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        if isinstance(self, Cache):
            self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """This function will display the history of calls of a function."""
    if method is None or not callable(method):
        return
    redis_store = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fn_name = method.__qualname__
    inputs = f'{fn_name}:inputs'
    outputs = f'{fn_name}:outputs'
    count = 0
    if redis_store.exists(fn_name):
        count = int(redis_store.get(fn_name))
    print(f'{fn_name} was called {count} times:')
    fn_inputs = redis_store.lrange(inputs, 0, -1)
    fn_outputs = redis_store.lrange(outputs, 0, -1)
    for i, o in zip(fn_inputs, fn_outputs):
        print(f'{fn_name}(*{i.decode("utf-8")}) -> {o.decode("utf-8")}')


class Cache:
    """This class is for the exercise of the course."""
    def __init__(self):
        """Constructor for the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
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
