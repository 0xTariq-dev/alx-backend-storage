#!/usr/bin/env python3
"""Module contains Python function that lists all documents in a collection"""


def list_all(mongo_collection):
    """Lists all documents in a mongodb collection"""
    return [doc for doc in mongo_collection.find()]
