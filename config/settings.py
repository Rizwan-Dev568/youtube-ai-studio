import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

OUTPUT_FOLDER = os.path.join(
    PROJECT_ROOT,
    "output"
)

DATA_FOLDER = os.path.join(
    PROJECT_ROOT,
    "data"
)

PROMPTS_FOLDER = os.path.join(
    PROJECT_ROOT,
    "prompts"
)

# ============================
# API Keys
# ============================

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ============================
# AI Configuration
# ============================

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

AI_TIMEOUT = 60

AI_MAX_RETRIES = 3

AI_MODELS = [

    # Primary
    "poolside/laguna-m.1:free",

    # Free Models
    "deepseek/deepseek-chat-v3-0324:free",

    "qwen/qwen3-235b-a22b:free",

    "google/gemma-3-27b-it:free",

    "meta-llama/llama-3.3-70b-instruct:free",

]