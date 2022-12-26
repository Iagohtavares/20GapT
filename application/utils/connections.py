from . import LOGIN, PASSWORD, SERVER

import redis
from pymongo import MongoClient
import MetaTrader5 as mt5


def to_redis():
    return redis.Redis(host='localhost', port=6379)


def to_mongo():
    return MongoClient(host='localhost', port=27017)


def to_mt():
    connected = mt5.initialize(login=LOGIN, password=PASSWORD, server=SERVER)

    if not connected:
        mt5.shutdown()
        return False

    logged = mt5.login(login=55572164, password="2mZ8u7tO&kO!", server="TickmillUK-Live")
    if not logged:
        return False
    return True
