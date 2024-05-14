#!/usr/bin/env python3
'''
Module contains Python script that provides some stats about Nginx logs
stored in MongoDB
'''
from pymongo import MongoClient


def filter_nginx_logs(nginx_logs):
    '''Filters nginx logs output from database collecion'''

    print('{} logs'.format(nginx_logs.count_documents({})))
    print('Methods:')

    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        method_count = len(list(nginx_logs.find({'method': method})))
        print('\tmethod {}: {}'.format(method, method_count))

    filters = {'method': 'GET', 'path': '/status'}
    status_route_visits = len(list(nginx_logs.find(filters)))
    print('{} status check'.format(status_route_visits))



def run():
    '''Configure Client and query logs data'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    filter_nginx_logs(client.logs.nginx)


if __name__ == '__main__':
    run()
