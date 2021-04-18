import logging

import redis

from app.core.enums import RedisStatus
from app.core.config import settings

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def redis_connect() -> redis.client.Redis:
    try:
        client = redis.Redis(
            host=settings.REDIS_URL.host,
            port=settings.REDIS_URL.port,
            password=settings.REDIS_URL.password,
            db=0,
            socket_timeout=5,
        )
        if not client.ping():
            raise redis.ConnectionError()
        logger.info("Redis client is connected to server.")
        update_status(RedisStatus.CONNECTED)
        return client
    except redis.AuthenticationError:
        logger.error("Unable to connect to redis server due to authentication error.")
        update_status(RedisStatus.AUTH_ERROR)
    except redis.ConnectionError:
        logger.error("Unable to communicate with redis server, no response recieved from PING message.")
        update_status(RedisStatus.CONN_ERROR)


def update_status(status: RedisStatus):
    settings.REDIS_CLIENT_STATUS = status


redis = redis_connect()
