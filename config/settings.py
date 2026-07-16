"""
Application Settings
"""

APP_NAME = "YouTube AI Studio"
VERSION = "1.0.0"

LOG_LEVEL = "INFO"

OUTPUT_FOLDER = "output"

import os
from dotenv import load_dotenv

load_dotenv()
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_FOLDER = os.path.join(PROJECT_ROOT, "output")
DATA_FOLDER = os.path.join(PROJECT_ROOT, "data")
PROMPTS_FOLDER = os.path.join(PROJECT_ROOT, "prompts")

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")