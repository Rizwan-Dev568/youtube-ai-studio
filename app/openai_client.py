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

    def ask(self, prompt, schema=None):

        logger.info("Starting AI Request")

        start_time = time.time()

        cached = self.cache.load(prompt)

        if cached:
            print("\nUsing Cached Response")
            logger.info("Using Cached Response")
            return cached

        errors = []

        for model in OPENROUTER_MODELS:

            print(f"\nTrying: {model}")

            try:

                response = self.client.chat.completions.create(

                    model=model,

                    temperature=0,

                    max_tokens=3000,

                    response_format={
                        "type": "json_object"
                    },

                    messages=[
                        {
                            "role": "system",
                            "content":
                            (
                                "You are a strict JSON API.\n"
                                "Return ONLY ONE valid JSON object.\n"
                                "Never use markdown.\n"
                                "Never explain.\n"
                                "Never output text before JSON.\n"
                                "Never output text after JSON.\n"
                                "Every required key must exist."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                result = response.choices[0].message.content

                if not result:
                    raise Exception("Empty AI response.")

                print("\n" + "=" * 80)
                print("RAW AI RESPONSE")
                print("=" * 80)
                print(result)
                print("=" * 80)

                logger.info(f"Success: {model}")
                logger.info(
                    f"Response Time: {time.time()-start_time:.2f} sec"
                )

                self.cache.save(
                    prompt,
                    result
                )

                return result

            except RateLimitError:

                print(f"Rate Limited: {model}")
                logger.warning(f"Rate Limited: {model}")

                errors.append(f"{model} -> Rate Limit")

                continue

            except APIError as e:

                msg = str(e)

                # Skip dead or unavailable models automatically
                if (
                    "404" in msg
                    or "No endpoints found" in msg
                    or "model not found" in msg.lower()
                ):

                    print(f"Skipping unavailable model: {model}")
                    logger.warning(f"Skipping {model}")

                    continue

                print(f"API Error: {model}")
                logger.error(msg)

                errors.append(f"{model} -> {msg}")

                continue

            except Exception as e:

                print(f"Failed: {model}")
                logger.exception(e)

                errors.append(f"{model} -> {e}")

                continue

        raise Exception(
            "\nNo working AI model found.\n\n"
            + "\n".join(errors)
        )