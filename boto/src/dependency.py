from aiogram import Bot

from src.api.repository import BotRepository
from src.api.service import BotService
from src.settings import settings


async def get_bot_repository() -> BotRepository:
    return BotRepository(tg_client=Bot(token=settings.TG_TOKEN))


async def get_bot_service(bot_repository: BotRepository) -> BotService:
    return BotService(bot_repository=bot_repository)
