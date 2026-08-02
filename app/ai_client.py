"""
Main AI Client Router
"""

from config.ai_provider import AI_PROVIDER

from app.openai_client import OpenAIClient


class AIClient:
    """
    Main AI Router

    Supported Providers:
    - OpenRouter
    - OpenAI
    - Gemini
    - Claude
    - Grok
    """

    def __init__(self):

        if AI_PROVIDER.lower() == "openrouter":

            self.client = OpenAIClient()

        else:

            raise Exception(
                f"Unsupported AI Provider: {AI_PROVIDER}"
            )

    def ask(
        self,
        prompt,
        schema=None
    ):

        return self.client.ask(
            prompt=prompt,
            schema=schema
        )