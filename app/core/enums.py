from enum import IntEnum


class RedisStatus(IntEnum):
    """Connection status for the redis client."""

    NONE = 0
    CONNECTED = 1
    AUTH_ERROR = 2
    CONN_ERROR = 3

    def __str__(self):
        return self.name


class RedisEvent(IntEnum):
    """Redis client events."""

    KEY_ADDED_TO_CACHE = 1
    KEY_FOUND_IN_CACHE = 2
    FAILED_TO_CACHE_KEY = 3

    def __str__(self):
        return self.name
