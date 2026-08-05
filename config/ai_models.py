"""
AI Model Configuration

Models are tried from top to bottom until one succeeds.
"""

OPENROUTER_MODELS = [

    # Fast & Reliable
    "moonshotai/kimi-k2:free",

    # Excellent JSON output
    "deepseek/deepseek-chat-v3-0324:free",

    # Large reasoning model
    "qwen/qwen3-235b-a22b:free",

    # Stable fallback
    "google/gemma-3-27b-it:free",

    # Final fallback
    "openai/gpt-oss-20b:free",

]