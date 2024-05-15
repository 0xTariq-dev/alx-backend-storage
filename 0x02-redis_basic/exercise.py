#!/usr/bin/env python3
"""This is a module for the exercise of the course."""

import redis
from uuid import uuid


class Exercise:
    """This class is for the exercise of the course."""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: str | bytes | int | float) -> str:
        """Store the data in the database."""
        key = str(uuid())
        self._redis.set(key, data)
        return key
