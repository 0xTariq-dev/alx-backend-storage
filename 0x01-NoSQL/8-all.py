#!/usr/bin/env python3
"""Module contains Python function that lists all documents in a collection"""

from pymongo.collection import Collection
from typing import List, Dict


def list_all(mongo_collection: Collection) -> List[Dict]:
    """Lists all documents in a mongodb collection"""
    return [doc for doc in mongo_collection.find()]
