import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN, NAS_ROOT_PATH, CATEGORIES
from handlers import commands, files, search, folders
from utils.storage import ensure_nas_structure

# Configure logging to be more professional
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def main():
    # 1. Initialize NAS structure
    ensure_nas_structure(NAS_ROOT_PATH, CATEGORIES)

    # 2. Initialize Bot and Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # 3. Register Routers
    dp.include_router(commands.router)
    dp.include_router(files.router)
    dp.include_router(search.router)
    dp.include_router(folders.router)

    # 4. Start Polling
    logger.info("--- Starting FileManagerBot ---")
    logger.info(f"NAS Root: {NAS_ROOT_PATH}")

    # Skip updates to avoid flooding on restart
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)
