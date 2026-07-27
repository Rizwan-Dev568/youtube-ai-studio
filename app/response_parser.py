"""
Response Parser

Converts AI JSON responses into Python dictionaries.
"""

import json
import re


class ResponseParser:

    @staticmethod
    def parse(text):
        """
        Parse AI response into a Python dictionary.
        """

        if text is None:
            raise ValueError("AI response is empty.")

        text = text.strip()

        # Remove markdown code blocks
        text = re.sub(r"^```json\s*", "", text)
        text = re.sub(r"^```\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

        text = text.strip()

        # Extract JSON object only
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            text = text[start:end + 1]

        # Fix invalid escaped dollar signs like \$1000
        text = text.replace(r"\$", "$")

        # Remove control characters
        text = re.sub(r"[\x00-\x1F]+", " ", text)

        try:
            return json.loads(text)

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON received from AI.\n\n{text}"
            ) from e