from enum import Enum

from redis import StrictRedis
from redis.connection import BlockingConnectionPool

pool = BlockingConnectionPool(host="redis", port=6379, decode_responses=True)
redis_client = StrictRedis(connection_pool=pool)

class Status(Enum):
    WAITING = "waiting"
    PAGE_SETUP = "Setting up page"
    GENERATING_SECTIONS = "Generating sections"
    GENERATING_CONTENT = "Generating content"
    COMPLETE = "complete"
    FAILED = "failed"

def update_status(page_id: str, status: Status):
    redis_client.hset(f"generation:{page_id}", "status", status.value)