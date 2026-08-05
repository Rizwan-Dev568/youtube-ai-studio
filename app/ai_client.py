"""
Main AI Client Router

Central entry point for all AI providers.
"""

from config.ai_provider import AI_PROVIDER

from app.openai_client import OpenAIClient


class AIClient:

    def __init__(self):

        provider = AI_PROVIDER.lower().strip()

        if provider == "openrouter":

            self.client = OpenAIClient()

        else:

            raise ValueError(
                f"Unsupported AI Provider: {AI_PROVIDER}"
            )

    # --------------------------------------------------
    # Low-Level Call
    # --------------------------------------------------

    def raw_ask(
        self,
        prompt,
        schema=None
    ):

        if not prompt:

            raise ValueError(
                "Prompt cannot be empty."
            )

        return self.client.ask(
            prompt=prompt,
            schema=schema
        )

    # --------------------------------------------------
    # High-Level Call
    # --------------------------------------------------

    def ask(
        self,
        prompt,
        schema=None
    ):

        return self.raw_ask(
            prompt,
            schema
        )