import asyncio
import os

import loguru
import django
from django.conf import settings
from aiogram.client.default import DefaultBotProperties

from loader import bot, dp


async def main():
    """Запуск бота"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

    django.setup()

    from handlers.routing import get_main_router
    
    try:
        dp.include_router(get_main_router())
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == '__main__':
    loguru.logger.info('Bot is starting')
    asyncio.run(main())
