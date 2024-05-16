#!/usr/bin/env python3
"""This module contains function get_page that returns the
content of a webpage."""

import redis
import requests
from functools import wraps
from typing import Callable


# Global redis instance
redis_client = redis.Redis()


def cache_result(method: Callable) -> Callable:
    """This decorator will Cache the fetched data."""
    @wraps(method)
    def wrapper(url: str) -> str:
        """Wrapper function for Caching requests output."""

        res = redis_client.get(f'result:{url}')

        if res:
            redis_client.incr(f'count:{url}')
            return res.decode('utf-8')
        res = method(url)
        redis_client.setex(f'count:{url}', 10, 1)
        redis_client.setex(f'result:{url}', 10, res)
        return res
    return wrapper


@cache_result
def get_page(url: str) -> str:
    """Return the content of a webpage after caching the response
    and track the request."""
    return requests.get(url).text
