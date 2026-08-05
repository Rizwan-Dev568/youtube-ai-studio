"""
Application Settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ==========================
# API Keys
# ==========================

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# ==========================
# OpenRouter
# ==========================

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# ==========================
# AI Settings
# ==========================

AI_TIMEOUT = 60
AI_MAX_RETRIES = 3
AI_MAX_TOKENS = 4000
AI_TEMPERATURE = 0