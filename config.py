import os
import sys
import logging
from dotenv import load_dotenv

# Configure basic logging for early startup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def get_env_or_exit(key: str, default: str = None, required: bool = True) -> str:
    """Helper to get environment variables or exit if required and missing."""
    value = os.getenv(key, default)
    if required and not value:
        logger.error(f"❌ MISSING CONFIGURATION: Environment variable '{key}' is not set.")
        sys.exit(1)
    return value

# --- Professional Config & Settings ---

# Bot Token from @BotFather
BOT_TOKEN = get_env_or_exit("BOT_TOKEN")

# Authorized Users (List of Telegram IDs)
# Supports single ID or comma-separated list
ALLOWED_USERS_RAW = get_env_or_exit("ALLOWED_USER_ID", default="0")
ALLOWED_USER_IDS = [int(uid.strip()) for uid in ALLOWED_USERS_RAW.split(",") if uid.strip().isdigit()]

def is_authorized(user_id: int) -> bool:
    return user_id in ALLOWED_USER_IDS

# NAS Storage Configuration
NAS_ROOT_PATH = get_env_or_exit("NAS_PATH", default="/mnt/nas")

# Storage Categories Configuration
# Format: { "Display Name": ["extensions", ...] }
CATEGORIES = {
    "Documents": [".pdf", ".docx", ".xlsx", ".txt", ".pptx", ".md"],
    "Media": [".png", ".jpg", ".jpeg", ".mp4", ".mov", ".gif", ".mkv", ".mp3", ".wav"],
    "Data": [".csv", ".json", ".sql", ".xml", ".yaml", ".yml"],
    "Scripts": [".py", ".sh", ".js", ".ts", ".go", ".c", ".cpp"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Other": []
}

# UI Settings
PAGE_SIZE = 10  # Number of files per page in browse mode
PROGRESS_BAR_LENGTH = 12
