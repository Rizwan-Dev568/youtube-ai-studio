from openai import OpenAI
from config.settings import OPENROUTER_API_KEY


class OpenAIClient:

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )

    def ask(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="poolside/laguna-m.1:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content