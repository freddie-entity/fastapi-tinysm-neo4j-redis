from typing import Optional
from aioredis import Redis, from_url
import os
from typing import Any, Optional, List, Tuple, Dict, Union

from config import settings

ReadMessageType = Tuple[bytes, bytes, Dict[bytes, bytes]]
RangeMessageType = Tuple[bytes, Dict[bytes, bytes]]

class CommandsMixin:
    async def xread(
        self, streams: List[str], timeout: int = 0, count: Optional[int] = None, latest_ids: Optional[List[str]] = None
    ) -> List[ReadMessageType]: ...
    async def xrange(
        self, stream: str, start: str = "-", stop: str = "+", count: Optional[int] = None
    ) -> List[RangeMessageType]: ...
    async def xrevrange(
        self, stream: str, start: str = "+", stop: str = "-", count: Optional[int] = None
    ) -> List[RangeMessageType]: ...
    async def xadd(self, stream: str, fields: Dict[str, Union[bytes, float, int, str]]) -> bytes: ...
    async def time(self) -> float: ...

class RedisCache(CommandsMixin):
    def __init__(self):
        self.redis_cache: Optional[Redis] = None
        
    async def init_cache(self):
        # self.redis_cache = await from_url("redis://redis-11622.c1.asia-northeast1-1.gce.cloud.redislabs.com:11622/0?encoding=utf-8",
        # host="tinysm-redis",
        # password="NGbgufgAK33ELiQdEJCLQqLmgIvcVBCA")
        self.redis_cache = await from_url(settings.DB_REDIS_CACHE)

    async def keys(self, pattern):
        return await self.redis_cache.keys(pattern)

    async def set(self, key, value):
        return await self.redis_cache.set(key, value)
    
    async def get(self, key):
        return await self.redis_cache.get(key)
    
    async def close(self):
        self.redis_cache.close()
        await self.redis_cache.wait_closed()

redis_cache = RedisCache()