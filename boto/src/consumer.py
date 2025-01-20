import asyncio
import logging

import aio_pika

from src.dependency import (
    get_bot_repository,
    get_bot_service,
)
from src.infrastructure.broker.rabbitmq import get_broker_connection


async def make_broker_connection():
    bot_repository = await get_bot_repository()
    bot_service = await get_bot_service(bot_repository=bot_repository)

    while True:
        try:
            connection = await get_broker_connection()
            channel = await connection.channel()
            logging.info("Connection established successfully")

            exchange = await channel.declare_exchange(
                name="marcelina_bot",
                type="direct",
                durable=True,
            )
            queue = await channel.declare_queue(
                name="marcelina_bot_queue",
                durable=True,
            )
            await queue.bind(exchange=exchange)

            await queue.consume(callback=bot_service.consume_event)
            logging.info("[!] Consumer bot is ready and waiting for messages.")

            await asyncio.Future()

        except (
            aio_pika.exceptions.AMQPConnectionError,
            aio_pika.exceptions.ChannelInvalidStateError,
        ) as e:
            logging.error(f"[!] Connection error: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)
