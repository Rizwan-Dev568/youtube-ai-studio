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
# OpenRouter Models
# ==========================

OPENROUTER_MODELS = [

    # Primary
    "poolside/laguna-m.1:free",

    # Free Fallbacks
    "mistralai/devstral-small:free",

    "moonshotai/kimi-k2:free",

    "z-ai/glm-4.5-air:free",

    "openai/gpt-oss-20b:free",

]