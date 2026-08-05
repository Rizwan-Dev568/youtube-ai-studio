"""
Professional Project Logger
"""

import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler


LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(exist_ok=True)

LOG_FILE = LOG_FOLDER / "youtube_ai_studio.log"


logger = logging.getLogger("YouTubeAIStudio")
logger.setLevel(logging.INFO)

logger.handlers.clear()


formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    "%Y-%m-%d %H:%M:%S"
)


file_handler = RotatingFileHandler(
    LOG_FILE,
    maxBytes=5 * 1024 * 1024,
    backupCount=5,
    encoding="utf-8"
)

file_handler.setFormatter(formatter)


console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)


logger.addHandler(file_handler)
logger.addHandler(console_handler)


logger.propagate = False