import os
import shutil
import math
import logging
import re
import time
from pathlib import Path
from typing import Optional, Dict, Union

logger = logging.getLogger(__name__)

_INVALID_NAME_CHARS = set('/\\\x00')
_MAX_FOLDER_NAME_LEN = 255

def get_disk_usage(path: Union[str, Path]) -> Optional[Dict[str, Union[int, float]]]:
    """Calculates disk usage for a given path with professional logging."""
    try:
        total, used, free = shutil.disk_usage(path)
        percent = (used / total) * 100
        return {
            "total": total,
            "used": used,
            "free": free,
            "percent": percent
        }
    except Exception as e:
        logger.error(f"Error calculating disk usage for {path}: {e}")
        return None

def generate_progress_bar(percent: float, length: int = 15) -> str:
    """Generates a modern text-based progress bar using '▰' and '▱' characters."""
    filled_length = int(round(length * percent / 100))
    # Using '▰' (U+25B0) for filled and '▱' (U+25B1) for empty
    bar = "▰" * filled_length + "▱" * (length - filled_length)
    return bar

def format_bytes(size_bytes: int) -> str:
    """Converts bytes to a human-readable format."""
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def sanitize_filename(filename: str) -> str:
    """Sanitizes the filename to prevent path traversal and ensure compatibility."""
    # Remove any path components
    filename = os.path.basename(filename)
    # Replace any character that isn't a word character, dot, or hyphen with an underscore
    filename = re.sub(r'[^\w\.\-]', '_', filename)
    # Ensure it's not empty
    if not filename:
        filename = "unnamed_file"
    return filename

def get_unique_path(target_path: Path) -> Path:
    """If file exists, appends a counter to the filename to make it unique."""
    if not target_path.exists():
        return target_path
    
    stem = target_path.stem
    suffix = target_path.suffix
    directory = target_path.parent
    counter = 1
    
    while True:
        new_path = directory / f"{stem} ({counter}){suffix}"
        if not new_path.exists():
            return new_path
        counter += 1

_rate_data: Dict[int, float] = {}

def is_rate_limited(user_id: int, min_interval: float = 2.0) -> bool:
    """Returns True if user has acted too recently and should be rate-limited."""
    now = time.time()
    if now - _rate_data.get(user_id, 0) < min_interval:
        return True
    _rate_data[user_id] = now
    return False

def safe_resolve(base: Path, rel_path: str) -> Optional[Path]:
    """Resolve rel_path against base, returning None if it escapes base directory."""
    try:
        resolved = (base / rel_path).resolve()
        resolved.relative_to(base.resolve())
        return resolved
    except (ValueError, OSError):
        return None

def validate_folder_name(name: str) -> Optional[str]:
    """Validate a folder name. Returns an error string or None if valid."""
    if not name:
        return "Name cannot be empty."
    if len(name) > _MAX_FOLDER_NAME_LEN:
        return f"Name too long (max {_MAX_FOLDER_NAME_LEN} characters)."
    if any(c in _INVALID_NAME_CHARS for c in name):
        return "Name contains invalid characters (/, \\, or null bytes)."
    if any(ord(c) < 32 for c in name):
        return "Name contains control characters."
    return None

def ensure_nas_structure(nas_path: str, categories: Dict):
    """Ensures the directory structure exists on the NAS with professional logging."""
    nas_root = Path(nas_path)
    if not nas_root.exists():
        logger.warning(f"NAS path '{nas_root}' does not exist. Creating...")
        nas_root.mkdir(parents=True, exist_ok=True)
    
    for category in categories:
        cat_path = nas_root / category
        if not cat_path.exists():
            cat_path.mkdir(exist_ok=True)
            logger.info(f"Created category folder: {cat_path}")
