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

        if text is None:
            raise ValueError("AI response is empty.")

        text = text.strip()

        # Remove Markdown JSON block
        if text.startswith("```json"):
            text = text.replace("```json", "", 1)

        if text.startswith("```"):
            text = text.replace("```", "", 1)

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        # Extract JSON if AI added extra text
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            text = text[start:end + 1]

        try:
            return json.loads(text)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON received from AI.\n\n{text}"
            ) from e