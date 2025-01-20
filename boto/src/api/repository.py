import asyncio
import logging
import os
from dataclasses import dataclass
from io import BytesIO

import aiofiles
from aiogram import Bot
from aiogram.types import BufferedInputFile
from PIL import Image

from src.api.schema import ScrapedDataSchema
from src.utils import (
    extract_domain,
    translator_text_to_ru,
)


@dataclass
class BotRepository:
    tg_client: Bot

    async def send_message(self, data: ScrapedDataSchema, chat_id: str):
        img_file_to_send = None

        try:
            if data.img_bytes:
                try:
                    img_file = BytesIO(data.img_bytes)
                    img = Image.open(img_file)
                    img_format = "PNG"
                    img_byte_arr = BytesIO()
                    img.save(img_byte_arr, format=img_format)
                    img_byte_arr.seek(0)
                    img_file_to_send = BufferedInputFile(
                        img_byte_arr.getvalue(),
                        filename=f"image.{img_format.lower()}",
                    )

                    logging.info("Image decoded success!")
                except Exception as e:
                    logging.warning(f"Image decoded failed: {img_file_to_send} - {e}")

                ad_url_domain = extract_domain(url=data.ad_url)
                domain = extract_domain(url=data.domain)
                text_ad = await asyncio.to_thread(translator_text_to_ru, data.text_ad) if data.text_ad else None
                geo = await asyncio.to_thread(translator_text_to_ru, data.geo) if data.geo else None

                message_text = (
                    f"<b>Гео:</b> {geo}\n"
                    f"<b>Домен:</b> <a href='{data.domain}'>{domain}</a>\n"
                    f"<b>Fingerprint:</b> {data.fingerprint}\n"
                    f"<b>Текст креатива:</b> {text_ad}\n"
                    f"<b>Ссылка куда ведет реклама:</b> <a href='{data.ad_url}'>{ad_url_domain}</a>\n"
                )

                logging.info("Image file decoded success!")

                await self.tg_client.send_photo(
                    chat_id=chat_id,
                    photo=img_file_to_send,
                    caption=message_text,
                    parse_mode="HTML",
                )
                logging.info("Message send to success!")

                await self._send_file(chat_id=chat_id, google_url=data.google_url)

                logging.info("File send to success!")
            else:
                logging.warning("Image file decoded failed")
        except Exception as e:
            logging.error(f"Error send_message: {e}")

    async def _send_file(self, chat_id: str, google_url: str):
        try:
            async with aiofiles.open("Link.txt", "w") as f:
                if google_url:
                    await f.write(google_url)
                else:
                    logging.warning("Google url NoneType")
                    await f.write("NoneType")

            async with aiofiles.open("Link.txt", "rb") as f:
                file_content = await f.read()
                file_input = BufferedInputFile(file_content, filename="Link.txt")

                await self.tg_client.send_document(
                    chat_id=chat_id,
                    document=file_input,
                    caption="Файлик с сохраненной ссылкой Google",
                )

            os.remove("Link.txt")
            logging.info("File Link.txt sent and removed successfully.")

        except Exception as e:
            logging.error(f"Unexpected send_file error: {e}")
