"""
Base Agent

All AI agents inherit from this class.
"""

from pathlib import Path

from app.ai_client import AIClient
from app.file_manager import FileManager
from app.response_parser import ResponseParser


class BaseAgent:

    schema = None

    def __init__(self):

        self.ai = AIClient()

    def load_prompt(self, filename):

        prompt_path = (
            Path(__file__).parent
            / "prompts"
            / filename
        )

        prompt = FileManager.read_text(prompt_path)

        print("\n" + "=" * 80)
        print(f"{filename.upper()} LOADED")
        print("=" * 80)
        print(prompt)
        print("=" * 80)

        return prompt

    def validate(self, data, schema):

        if not isinstance(data, dict):
            raise Exception("AI did not return a JSON object.")

        for key, expected_type in schema.items():

            if key not in data:
                raise Exception(f"Missing key: {key}")

            if not isinstance(data[key], expected_type):
                raise Exception(
                    f"'{key}' should be {expected_type.__name__}, "
                    f"got {type(data[key]).__name__}"
                )

        return True

    def ask(self, prompt, schema=None):

        if schema is None:
            schema = self.schema

        last_error = None

        for attempt in range(3):

            print(f"\nAI Attempt {attempt + 1}/3")

            try:

                response = self.ai.ask(
                    prompt,
                    schema=schema
                )

                if response is None:
                    raise Exception(
                        "Empty AI response."
                    )

                print("\n======================")
                print("TYPE OF RESPONSE")
                print("======================")
                print(type(response))
                print(response)
                print("======================\n")

                data = ResponseParser.parse(response)

                print("\n======================")
                print("PARSED JSON")
                print("======================")
                print(data)
                print("======================\n")

                if schema is not None:
                    self.validate(
                        data,
                        schema
                    )

                return data

            except Exception as e:

                print(f"\nAttempt {attempt + 1} Failed")
                print(e)

                last_error = e

        raise Exception(
            f"\nAI failed after 3 attempts.\n\n{last_error}"
        )