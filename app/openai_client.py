from openai import OpenAI
from openai import APIError
from openai import RateLimitError

from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    AI_MODELS,
)


class OpenAIClient:

    def __init__(self):

        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
        )

    def ask(self, prompt):

        last_error = None

        for model in AI_MODELS:

            try:

                print(f"\nTrying: {model}")

                response = self.client.chat.completions.create(

                    model=model,

                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                print(f"Success: {model}")

                return response.choices[0].message.content

            except RateLimitError as e:

                print(f"Rate Limit: {model}")

                last_error = e

            except APIError as e:

                print(f"API Error: {model}")

                last_error = e

            except Exception as e:

                print(f"Failed: {model}")

                last_error = e

        raise Exception(
            f"\nAll AI models failed.\n\n{last_error}"
        )