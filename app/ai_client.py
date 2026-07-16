class AIClient:
    """
    Base AI Client

    Future Providers:
    - OpenAI
    - Gemini
    - Claude
    - Grok
    """

    def ask(self, prompt: str):
        raise NotImplementedError("Provider not implemented.")