"""
Base Agent

All AI agents inherit from this class.
"""

from pathlib import Path

from app.ai_client import AIClient
from app.file_manager import FileManager
from app.response_parser import ResponseParser
from app.json_repair_service import JsonRepairService

from memory.memory_manager import MemoryManager


class BaseAgent:

    schema = None

    MAX_RETRIES = 3

    def __init__(self):

        self.ai = AIClient()
        self.memory = MemoryManager()
        self.json_repair = JsonRepairService()

    def load_prompt(self, filename):

        prompt_path = (
            Path(__file__).parent
            / "prompts"
            / filename
        )

        return FileManager.read_text(
            prompt_path
        )

    def validate(self, data, schema):

        if not isinstance(data, dict):
            raise Exception(
                "AI did not return a JSON object."
            )

        for key, expected_type in schema.items():

            if key not in data:

                raise Exception(
                    f"Missing key: {key}"
                )

            if not isinstance(
                data[key],
                expected_type
            ):

                raise Exception(
                    f"'{key}' should be "
                    f"{expected_type.__name__}, "
                    f"got {type(data[key]).__name__}"
                )

        return True

    def ask(
        self,
        prompt,
        schema=None
    ):

        if schema is None:
            schema = self.schema

        last_error = None

        for attempt in range(
            self.MAX_RETRIES
        ):

            print(
                f"\nAI Attempt {attempt + 1}/{self.MAX_RETRIES}"
            )

            try:

                response = self.ai.ask(
                    prompt,
                    schema=schema
                )

                if not response:

                    raise Exception(
                        "Empty AI response."
                    )

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

                if schema:

                    self.validate(
                        data,
                        schema
                    )

                self.memory.set(
                    "last_response",
                    data
                )

                return data

            except Exception as e:

                print(
                    f"\nAttempt {attempt + 1} Failed"
                )

                print(e)

                last_error = e

                try:

                    self.ai.client.cache.delete(
                        prompt
                    )

                except Exception:
                    pass

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