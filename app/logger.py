"""
Project Logger
"""

import logging
from pathlib import Path


LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(exist_ok=True)

LOG_FILE = LOG_FOLDER / "youtube_ai_studio.log"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)


logger = logging.getLogger("YouTubeAIStudio")