"""
AI Model Configuration

Models are tried from top to bottom until one succeeds.
"""

OPENROUTER_MODELS = [

    # Primary (Fast + Reliable)
    "openai/gpt-oss-20b:free",

    # Fallbacks
    "moonshotai/kimi-k2:free",
    "deepseek/deepseek-chat-v3-0324:free",
    "qwen/qwen3-235b-a22b:free",
    "google/gemma-3-27b-it:free",
]