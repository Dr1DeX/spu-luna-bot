import aio_pika

from src.settings import settings


async def get_broker_connection() -> aio_pika.abc.AbstractConnection:
    return await aio_pika.connect_robust(url=settings.BROKER_URL)
