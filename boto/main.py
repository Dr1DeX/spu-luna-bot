import asyncio
import logging

from src.consumer import make_broker_connection


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    await make_broker_connection()
    logging.info("[!]Starting consumer bot")


if __name__ == "__main__":
    asyncio.run(main())
