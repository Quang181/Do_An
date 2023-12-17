import redis
import os


class Redis:
    REDIS_DB = os.getenv('REDIS_URL', 'redis://localhost:6379')


def get_redis():
    connect = redis.Redis(host='localhost', port=6379, db=0)
    return connect
