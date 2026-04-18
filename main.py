import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN, NAS_ROOT_PATH, CATEGORIES
from handlers import commands, files, search, folders, trash
from utils.storage import ensure_nas_structure

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def main():
    ensure_nas_structure(NAS_ROOT_PATH, CATEGORIES)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(commands.router)
    dp.include_router(files.router)
    dp.include_router(search.router)
    dp.include_router(folders.router)
    dp.include_router(trash.router)

    logger.info("--- Starting NAS Manager Bot ---")
    logger.info(f"NAS Root: {NAS_ROOT_PATH}")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped.")
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
