#!/usr/bin/env python3
"""Module contains Python script that provides some stats about Nginx logs
stored in MongoDB"""
from pymongo import MongoClient


def filter_nginx_logs(nginx_logs):
    """Filters nginx logs output from database collecion"""
    print(f"{nginx_logs.count_documents({})} logs")
    print("Methods:")
    for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        method_count = len(list(nginx_logs.find({"method": method})))
        print(f"\tmethod {method}: {method_count}")
    status_route_visits = len(list(
        nginx_logs.find({'method': 'GET', 'path': '/status'})
        ))
    print(f'{status_route_visits} status check')


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    filter_nginx_logs(client.logs.nginx)
