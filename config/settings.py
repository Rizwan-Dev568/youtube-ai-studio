"""
Global Project Settings

Central configuration for the
YouTube AI Studio.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# API Keys
# ==================================================

OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY",
    ""
)

YOUTUBE_API_KEY = os.getenv(
    "YOUTUBE_API_KEY",
    ""
)

# ==================================================
# OpenRouter
# ==================================================

OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1"
)

# ==================================================
# AI
# ==================================================

AI_MAX_RETRIES = 3

AI_MAX_TOKENS = 8000

AI_TEMPERATURE = 0.7

# Backward Compatibility
MAX_RETRIES = AI_MAX_RETRIES

USE_CACHE = True

AUTO_RESUME = True

SAVE_INTERMEDIATE = True

# ==================================================
# Workflow
# ==================================================

BATCH_SIZE = 5

MAX_SCENES = 100

# ==================================================
# Image
# ==================================================

DEFAULT_IMAGE_STYLE = (
    "Cinematic Realistic"
)

DEFAULT_ASPECT_RATIO = (
    "16:9"
)

# ==================================================
# Video
# ==================================================

DEFAULT_VIDEO_DURATION = (
    "8 seconds"
)

# ==================================================
# Output
# ==================================================

SAVE_JSON = True

SAVE_MARKDOWN = True

SAVE_TEXT = True

# ==================================================
# Logging
# ==================================================

LOG_AI_REQUESTS = True

LOG_TOKEN_USAGE = True

LOG_EXECUTION_TIME = True

# ==================================================
# Future
# ==================================================

ENABLE_COST_TRACKER = False

ENABLE_BATCH_PROCESSING = False

ENABLE_CHARACTER_LOCK = True