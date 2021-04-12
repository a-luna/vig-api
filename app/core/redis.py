import redis
import sys

from app.core.config import settings


def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host=settings.REDIS_URL.host,
            port=settings.REDIS_URL.port,
            password=settings.REDIS_URL.password,
            db=0,
            socket_timeout=5,
        )
        ping = client.ping()
        if ping is True:
            return client
    except redis.AuthenticationError:
        print("AuthenticationError")
        sys.exit(1)


client = redis_connect()


def get_cached_response(key: str) -> str:
    return client.get(key)


def cache_response(key: str, value: str) -> bool:
    return client.set(name=key, value=value)
