from openai import OpenAI
from openai import APIError
from openai import RateLimitError

import time

from app.logger import logger
from cache.cache_manager import CacheManager

from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    AI_MAX_RETRIES,
    AI_MAX_TOKENS,
    AI_TEMPERATURE,
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

        logger.info("=" * 80)
        logger.info("NEW AI REQUEST")
        logger.info("=" * 80)

        start_time = time.time()

        cached = self.cache.load(prompt)

        if cached is not None:

            print("\nUsing Cached Response")
            logger.info("Cache Hit")

            return cached

        errors = []

        for model in OPENROUTER_MODELS:

            print(f"\nTrying Model: {model}")
            logger.info(f"Trying Model: {model}")

            for attempt in range(
                1,
                AI_MAX_RETRIES + 1
            ):

                print(
                    f"Attempt {attempt}/{AI_MAX_RETRIES}"
                )

                try:

                    response = self.client.chat.completions.create(

                        model=model,

                        temperature=AI_TEMPERATURE,

                        max_tokens=AI_MAX_TOKENS,

                        response_format={
                            "type": "json_object"
                        },

                        messages=[
                            {
                                "role": "system",
                                "content": (
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

                    choice = response.choices[0]

                    finish_reason = choice.finish_reason

                    if finish_reason != "stop":

                        raise Exception(
                            f"Incomplete AI response (finish_reason={finish_reason})"
                        )

                    result = choice.message.content

                    if result is None:

                        raise Exception(
                            "Empty AI response."
                        )

                    result = str(result).strip()

                    if result == "":

                        raise Exception(
                            "Blank AI response."
                        )

                    print("\n" + "=" * 80)
                    print("RAW AI RESPONSE")
                    print("=" * 80)
                    print(result)
                    print("=" * 80)

                    logger.info(
                        f"Success: {model}"
                    )

                    logger.info(
                        f"Response Time: {time.time() - start_time:.2f} sec"
                    )

                    self.cache.save(
                        prompt,
                        result
                    )

                    return result
                except RateLimitError as e:

                    logger.warning(
                        f"Rate Limited: {model}"
                    )

                    print(
                        f"Rate Limited: {model}"
                    )

                    errors.append(
                        f"{model} -> Rate Limit -> {e}"
                    )

                    if attempt < AI_MAX_RETRIES:

                        time.sleep(2)

                        continue

                    break

                except APIError as e:

                    msg = str(e)

                    logger.error(msg)

                    print(msg)

                    errors.append(
                        f"{model} -> {msg}"
                    )

                    msg_lower = msg.lower()

                    if (
                        "404" in msg
                        or "no endpoints found" in msg_lower
                        or "model not found" in msg_lower
                    ):

                        print(
                            f"Skipping unavailable model: {model}"
                        )

                        break

                    if (
                        "401" in msg
                        or "authentication_error" in msg_lower
                        or "invalid api key" in msg_lower
                    ):

                        print(
                            f"Authentication failed: {model}"
                        )

                        break

                    if attempt < AI_MAX_RETRIES:

                        time.sleep(2)

                        continue

                    break

                except Exception as e:

                    logger.exception(e)

                    print(
                        f"Failed: {model}"
                    )

                    errors.append(
                        f"{model} -> {e}"
                    )

                    if attempt < AI_MAX_RETRIES:

                        time.sleep(2)

                        continue

                    break

        logger.error(
            "All AI models failed."
        )

        raise Exception(
            "\nNo working AI model found.\n\n"
            + "\n".join(errors)
        )    