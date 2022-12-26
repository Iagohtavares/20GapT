import redis
from pymongo import MongoClient

STD = 0.000623
HIGHER_FACTOR = 1.0
LOWER_FACTOR = 1.0


def function(t, const_t3=None, const_t2=None, const_t1=None, const_t0=None) -> float:
    # funcao_modelo = -((0.000000001)(t^3)) + ((0.0000001)(t^2)) + ((0.00002)*(t)) + 0.0001;
    const_t3 = -0.000000001
    const_t2 = 0.0000001
    const_t1 = 0.00002
    const_t0 = 0.0001

    return const_t3*(t*t*t) + const_t2*(t*t) + const_t1*t + const_t0


def to_redis():
    return redis.Redis(host='redis', port=6379)


def to_mongo():
    return MongoClient(host='mongo', port=27017)
