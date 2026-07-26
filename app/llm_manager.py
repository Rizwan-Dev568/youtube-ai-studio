from app.openai_client import OpenAIClient


class LLMManager:

    def __init__(self):

        self.providers = {
            "openrouter": OpenAIClient(),
        }

    def ask(self, prompt, provider="openrouter"):

        if provider not in self.providers:
            raise Exception(f"Unknown provider: {provider}")

        return self.providers[provider].ask(prompt)