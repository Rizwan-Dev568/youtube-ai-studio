from config.ai_provider import AI_PROVIDER

from app.openai_client import OpenAIClient


class AIClient:
    """
    Main AI Router

    Supported Providers:
    - OpenRouter
    - Gemini
    - OpenAI
    - Claude
    - Grok
    """

    def __init__(self):

        if AI_PROVIDER == "openrouter":
            self.client = OpenAIClient()

        else:
            raise Exception(
                f"Unsupported AI Provider: {AI_PROVIDER}"
            )

    def ask(self, prompt: str):
        return self.client.ask(prompt)