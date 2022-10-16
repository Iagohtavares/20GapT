import redis
from pymongo import MongoClient


def redis_connection():
    return redis.Redis(host='redis', port=6379)


def mongo_connection():
    return MongoClient(host='mongo', port=27017)
