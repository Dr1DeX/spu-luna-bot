import base64
import json
import logging
from dataclasses import dataclass

import aio_pika.abc

from src.api.repository import BotRepository
from src.api.schema import ScrapedDataSchema
from src.settings import settings
from src.utils import get_img_base64_to_s3


@dataclass
class BotService:
    bot_repository: BotRepository

    async def consume_event(self, msg: aio_pika.abc.AbstractIncomingMessage):
        try:
            async with msg.process():
                data_body = json.loads(msg.body.decode())

                logging.info(f"Received data: {data_body}")

                parsed_data: dict = data_body.get("data")

                img_base64 = await get_img_base64_to_s3(rk_id=parsed_data.get("rk_id"))

                if img_base64:
                    img_bytes = base64.b64decode(img_base64)
                    parsed_info = ScrapedDataSchema(**parsed_data, img_bytes=img_bytes)

                    logging.debug(f"Parsed Info: {parsed_info}")

                    await self.bot_repository.send_message(data=parsed_info, chat_id=settings.CHAT_ID)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
