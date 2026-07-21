"""
Response Parser

Converts AI JSON responses into Python dictionaries.
"""

import json


class ResponseParser:

    @staticmethod
    def parse(text):
        """
        Parse AI response into a Python dictionary.
        """

        text = text.strip()

        # Remove Markdown JSON block if present
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.startswith("```"):
            text = text.replace("```", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        try:
            return json.loads(text)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON received from AI.\n\n{text}"
            ) from e