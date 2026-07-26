"""
AI Model Configuration

Central place for all AI providers and models.
"""


OPENROUTER_MODELS = [

    # Primary
    "poolside/laguna-m.1:free",

    # Fallbacks
    "deepseek/deepseek-chat-v3-0324:free",

    "qwen/qwen3-235b-a22b:free",

    "google/gemma-3-27b-it:free",

    "meta-llama/llama-3.3-70b-instruct:free",

]