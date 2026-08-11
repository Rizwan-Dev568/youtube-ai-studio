"""
OpenRouter AI Client

Central OpenRouter client used by all AI agents.

Supports:
- Model fallback
- JSON object responses
- JSON Schema structured outputs
- Response caching
- Rate-limit handling
- API error handling
- Automatic model disabling
"""

import time

from openai import OpenAI
from openai import APIError
from openai import RateLimitError

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
from config.model_manager import ModelManager


class OpenAIClient:

    def __init__(self):

        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL,
        )

        self.cache = CacheManager()

        self.model_manager = ModelManager()

    # --------------------------------------------------
    # Python Schema -> JSON Schema
    # --------------------------------------------------

    def _python_schema_to_json_schema(
        self,
        schema,
    ):

        if isinstance(
            schema,
            type
        ):

            mapping = {
                str: "string",
                int: "integer",
                float: "number",
                bool: "boolean",
            }

            if schema not in mapping:

                raise ValueError(
                    f"Unsupported schema type: {schema}"
                )

            return {
                "type": mapping[schema]
            }

        if isinstance(
            schema,
            dict
        ):

            properties = {}

            for key, value in schema.items():

                properties[key] = (
                    self._python_schema_to_json_schema(
                        value
                    )
                )

            return {
                "type": "object",
                "properties": properties,
                "required": list(
                    schema.keys()
                ),
                "additionalProperties": False,
            }

        if isinstance(
            schema,
            list
        ):

            if not schema:

                return {
                    "type": "array"
                }

            return {
                "type": "array",
                "items": (
                    self._python_schema_to_json_schema(
                        schema[0]
                    )
                ),
            }

        raise ValueError(
            f"Unsupported schema value: {schema}"
        )

    # --------------------------------------------------
    # Response Format
    # --------------------------------------------------

    def _build_response_format(
        self,
        schema,
    ):

        if schema is None:

            return {
                "type": "json_object"
            }

        json_schema = (
            self._python_schema_to_json_schema(
                schema
            )
        )

        return {
            "type": "json_schema",
            "json_schema": {
                "name": "ai_response",
                "strict": True,
                "schema": json_schema,
            },
        }

    # --------------------------------------------------
    # Ask
    # --------------------------------------------------

    def ask(
        self,
        prompt,
        schema=None
    ):

        logger.info("=" * 80)
        logger.info("NEW AI REQUEST")
        logger.info("=" * 80)

        if not prompt:

            raise ValueError(
                "Prompt cannot be empty."
            )

        start_time = time.time()

        cached = self.cache.load(
            prompt
        )

        if cached is not None:

            print(
                "\nUsing Cached Response"
            )

            logger.info(
                "Cache Hit"
            )

            return cached

        errors = []

        response_format = (
            self._build_response_format(
                schema
            )
        )

        for model in self.model_manager.get_models():

            print(
                f"\nTrying Model: {model}"
            )

            logger.info(
                f"Trying Model: {model}"
            )

            for attempt in range(
                1,
                AI_MAX_RETRIES + 1
            ):

                print(
                    f"Attempt "
                    f"{attempt}/{AI_MAX_RETRIES}"
                )

                try:

                    response = (
                        self.client.chat.completions.create(

                            model=model,

                            temperature=AI_TEMPERATURE,

                            max_tokens=AI_MAX_TOKENS,

                            response_format=(
                                response_format
                            ),

                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "You are a strict "
                                        "JSON API.\n"
                                        "Return ONLY ONE "
                                        "valid JSON object.\n"
                                        "Never use markdown.\n"
                                        "Never explain.\n"
                                        "Never output text "
                                        "before JSON.\n"
                                        "Never output text "
                                        "after JSON.\n"
                                        "Every required key "
                                        "must exist.\n"
                                        "Every value must "
                                        "match the requested "
                                        "schema type exactly."
                                    ),
                                },
                                {
                                    "role": "user",
                                    "content": prompt,
                                },
                            ],
                        )
                    )

                    if response is None:

                        raise Exception(
                            "OpenAI returned None."
                        )

                    if response.choices is None:

                        raise Exception(
                            "OpenAI returned no choices."
                        )

                    if len(
                        response.choices
                    ) == 0:

                        raise Exception(
                            "OpenAI returned an empty "
                            "choices list."
                        )

                    choice = (
                        response.choices[0]
                    )

                    if choice is None:

                        raise Exception(
                            "First choice is None."
                        )

                    if choice.message is None:

                        raise Exception(
                            "Choice message is None."
                        )

                    finish_reason = (
                        choice.finish_reason
                    )

                    if finish_reason != "stop":

                        raise Exception(
                            "Incomplete AI response "
                            f"(finish_reason="
                            f"{finish_reason})"
                        )

                    result = getattr(
                        choice.message,
                        "content",
                        None
                    )

                    if result is None:

                        raise Exception(
                            "Message content is None."
                        )

                    if not isinstance(
                        result,
                        str
                    ):

                        result = str(
                            result
                        )

                    result = result.strip()

                    if not result:

                        raise Exception(
                            "Blank AI response."
                        )

                    print(
                        "\n" + "=" * 80
                    )

                    print(
                        "RAW AI RESPONSE"
                    )

                    print(
                        "=" * 80
                    )

                    print(
                        result
                    )

                    print(
                        "=" * 80
                    )

                    logger.info(
                        f"Success: {model}"
                    )

                    logger.info(
                        "Response Time: "
                        f"{time.time() - start_time:.2f} sec"
                    )

                    self.model_manager.save()

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
                        f"{model} -> "
                        f"Rate Limit -> {e}"
                    )

                    if (
                        attempt
                        <
                        AI_MAX_RETRIES
                    ):

                        time.sleep(2)

                        continue

                    break

                except APIError as e:

                    msg = str(e)

                    logger.error(
                        msg
                    )

                    print(
                        msg
                    )

                    errors.append(
                        f"{model} -> {msg}"
                    )

                    msg_lower = (
                        msg.lower()
                    )

                    if (
                        "404" in msg
                        or "no endpoints found"
                        in msg_lower
                        or "model not found"
                        in msg_lower
                        or "unavailable for free"
                        in msg_lower
                    ):

                        print(
                            "Skipping unavailable "
                            f"model: {model}"
                        )

                        logger.warning(
                            "Removing unavailable "
                            f"model: {model}"
                        )

                        self.model_manager.remove_model(
                            model
                        )

                        break

                    if (
                        "401" in msg
                        or "authentication_error"
                        in msg_lower
                        or "invalid api key"
                        in msg_lower
                    ):

                        print(
                            "Authentication failed: "
                            f"{model}"
                        )

                        break

                    if (
                        attempt
                        <
                        AI_MAX_RETRIES
                    ):

                        time.sleep(2)

                        continue

                    break

                except Exception as e:

                    logger.exception(
                        e
                    )

                    print(
                        f"Failed: {model}"
                    )

                    errors.append(
                        f"{model} -> {e}"
                    )

                    if (
                        attempt
                        <
                        AI_MAX_RETRIES
                    ):

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