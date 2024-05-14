#!/usr/bin/env python3
"""Module contains Python script that provides some stats about Nginx logs
stored in MongoDB"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = client.logs.nginx

    print(f"{nginx_logs.count_documents({})} logs\nMethods:")
    for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        method_count = nginx_logs.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")
    print(f'{nginx_logs.count_documents({"path": "/status"})} status check')
