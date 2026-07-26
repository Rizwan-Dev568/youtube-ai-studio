from openai import OpenAI
from openai import APIError
from openai import RateLimitError

import time

from app.logger import logger
from cache.cache_manager import CacheManager

from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
)

from config.ai_models import OPENROUTER_MODELS


class OpenAIClient:

    def __init__(self):

        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
        )

        self.cache = CacheManager()

    def ask(self, prompt):

        logger.info("Starting AI Request")

        start_time = time.time()

        cached = self.cache.load(prompt)

        if cached is not None:

            logger.info("Using Cached Response")

            print("\nUsing Cached Response")

            return cached

        errors = []

        for model in OPENROUTER_MODELS:

            try:

                print(f"\nTrying: {model}")

                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ]
                )

                print(f"Success: {model}")

                logger.info(f"Success: {model}")

                result = response.choices[0].message.content

                self.cache.save(
                    prompt,
                    result
                )

                logger.info(
                    f"Response Time: {time.time() - start_time:.2f} sec"
                )

                return result

            except RateLimitError:

                logger.warning(f"Rate Limited: {model}")

                print(f"Rate Limited: {model}")

                errors.append(f"{model} -> Rate Limit")

            except APIError as e:

                logger.error(f"{model} -> {e}")

                print(f"API Error: {model}")

                errors.append(f"{model} -> {e}")

            except Exception as e:

                logger.exception(e)

                print(f"Failed: {model}")

                errors.append(f"{model} -> {e}")

        raise Exception(
            "No AI model is currently available.\n\n"
            + "\n".join(errors)
        )