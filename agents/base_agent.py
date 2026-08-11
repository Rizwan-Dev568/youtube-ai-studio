"""
Base Agent

All AI agents inherit from this class.
"""

from app.ai_client import AIClient
from app.prompt_manager import PromptManager
from app.response_parser import ResponseParser
from app.json_repair_service import JsonRepairService
from app.deep_validator import DeepValidator
from memory.memory_manager import MemoryManager


class BaseAgent:

    schema = None

    MAX_RETRIES = 3

    def __init__(self):

        self.ai = AIClient()
        self.prompt_manager = PromptManager()
        self.memory = MemoryManager()
        self.json_repair = JsonRepairService()

    def load_prompt(
        self,
        filename
    ):

        return self.prompt_manager.load(
            filename
        )

    def validate(
        self,
        data,
        schema
    ):

        if not isinstance(
            data,
            dict
        ):

            raise Exception(
                "AI did not return a JSON object."
            )

        DeepValidator.validate(
            data,
            schema
        )

        return True

    def _build_retry_prompt(
        self,
        original_prompt,
        error
    ):

        return (
            f"{original_prompt}\n\n"
            "IMPORTANT CORRECTION:\n"
            "The previous AI response failed "
            "validation.\n\n"
            f"Validation error:\n{error}\n\n"
            "Generate a completely corrected "
            "JSON response.\n"
            "Do not omit any required key.\n"
            "Do not rename any required key.\n"
            "Do not add unexpected keys.\n"
            "Every value must match the required "
            "schema type exactly.\n"
            "Return ONLY the JSON object."
        )

    def ask(
        self,
        prompt,
        schema=None,
        quality_validator=None,
        quality_type=None,
        quality_callback=None
    ):

        if schema is None:

            schema = self.schema

        last_error = None

        current_prompt = prompt

        for attempt in range(
            self.MAX_RETRIES
        ):

            print(
                f"\nAI Attempt "
                f"{attempt + 1}/{self.MAX_RETRIES}"
            )

            try:

                response = self.ai.ask(
                    current_prompt,
                    schema=schema
                )

                if not response:

                    raise Exception(
                        "Empty AI response."
                    )

                # ----------------------------------
                # Parse JSON
                # ----------------------------------

                try:

                    data = ResponseParser.parse(
                        response
                    )

                except Exception:

                    print(
                        "\nRepairing malformed JSON..."
                    )

                    repaired = (
                        self.json_repair.repair(
                            response
                        )
                    )

                    data = ResponseParser.parse(
                        repaired
                    )

                # ----------------------------------
                # Schema Validation
                # ----------------------------------

                if schema:

                    self.validate(
                        data,
                        schema
                    )

                # ----------------------------------
                # Quality Validation
                # ----------------------------------

                if quality_validator:

                    if quality_type == "images":

                        quality_validator.validate_images(
                            data.get(
                                "images",
                                []
                            )
                        )

                    elif quality_type == "videos":

                        quality_validator.validate_videos(
                            data.get(
                                "videos",
                                []
                            )
                        )

                    elif quality_type == "voice":

                        if quality_callback is None:

                            raise Exception(
                                "Voice quality callback "
                                "is required."
                            )

                        quality_callback(
                            data
                        )

                    else:

                        raise Exception(
                            "Unknown quality validation "
                            "type: "
                            f"{quality_type}"
                        )

                    print(
                        "\n✓ Prompt Quality Passed"
                    )

                # ----------------------------------
                # Save Successful Response
                # ----------------------------------

                self.memory.set(
                    "last_response",
                    data
                )

                return data

            except Exception as e:

                print(
                    f"\nAttempt "
                    f"{attempt + 1} Failed"
                )

                print(
                    f"Validation/Error: {e}"
                )

                last_error = e

                # ----------------------------------
                # Delete Bad Cache
                # ----------------------------------

                try:

                    self.ai.client.cache.delete(
                        current_prompt
                    )

                    print(
                        "\n✓ Bad cached response deleted."
                    )

                except Exception:

                    pass

                # ----------------------------------
                # Retry Preparation
                # ----------------------------------

                if (
                    attempt
                    <
                    self.MAX_RETRIES - 1
                ):

                    current_prompt = (
                        self._build_retry_prompt(
                            prompt,
                            str(e)
                        )
                    )

                    print(
                        "\nRetrying AI generation "
                        "with validation feedback..."
                    )

                    continue

        raise Exception(
            f"\nAI failed after "
            f"{self.MAX_RETRIES} attempts.\n\n"
            f"{last_error}"
        )

    def recall(
        self,
        key,
        default=None
    ):

        return self.memory.get(
            key,
            default
        )