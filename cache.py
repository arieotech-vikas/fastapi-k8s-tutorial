# import redis

# redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


import os
import redis

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
