import logging
import re

import httpx
from deep_translator import GoogleTranslator

from src.settings import settings


def extract_domain(url: str) -> str:
    match = re.search(r"https?://([A-Za-z_0-9.-]+).*", url)
    return match.group(1) if match else url


async def get_img_base64_to_s3(rk_id: str) -> str:
    payload = {"rk_id": rk_id, "file_extension": "PNG"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=settings.S3_API, params=payload, timeout=30000)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logging.error(f"Unexpected error get_img_base64: {e}")
            raise


def translator_text_to_ru(text: str) -> str:
    translated_text = GoogleTranslator(source="auto", target="ru").translate(text=text)
    return translated_text
