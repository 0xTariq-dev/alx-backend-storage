#!/usr/bin/env python3
"""This is a module for the exercise of the course."""

import redis
from uuid import uuid4 as uuid
from typing import Union


class Cache:
    """This class is for the exercise of the course."""
    def __init__(self):
        """Constructor for the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data in the database."""
        key = str(uuid())
        self._redis.set(key, data)
        return key
