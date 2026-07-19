from app.openai_client import OpenAIClient


class AIClient:
    """
    Main AI Client

    Future Providers:
    - OpenAI/OpenRouter
    - Gemini
    - Claude
    - Grok
    """

    def __init__(self):
        self.client = OpenAIClient()

    def ask(self, prompt: str):
        return self.client.ask(prompt)