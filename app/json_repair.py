"""
Professional JSON Repair Utility
"""

import json
import re


class JsonRepair:

    @staticmethod
    def repair(text):

        if text is None:
            return None

        if not isinstance(text, str):
            return text

        text = text.strip()

        # Remove markdown
        text = re.sub(r"^```json", "", text, flags=re.I)
        text = re.sub(r"^```", "", text)
        text = re.sub(r"```$", "", text)

        # Keep only JSON
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            text = text[start:end + 1]

        # Remove trailing commas
        text = re.sub(r",(\s*[}\]])", r"\1", text)

        # Replace smart quotes
        text = (
            text.replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
        )

        # Remove invalid control chars
        text = re.sub(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F]",
            "",
            text
        )

        return text.strip()

    @staticmethod
    def loads(text):

        repaired = JsonRepair.repair(text)

        print("\n======================")
        print("JSON AFTER REPAIR")
        print("======================")
        print(repaired)
        print("======================\n")

        try:
            return json.loads(repaired)

        except json.JSONDecodeError as e:

            print("\nFirst JSON Parse Failed")
            print(e)

            repaired = JsonRepair.second_pass(repaired)

            print("\n======================")
            print("JSON AFTER SECOND PASS")
            print("======================")
            print(repaired)
            print("======================\n")

            return json.loads(repaired)

    @staticmethod
    def second_pass(text):

        # Remove trailing commas again
        text = re.sub(r",(\s*[}\]])", r"\1", text)

        # Close array if missing
        text = re.sub(
            r'("sections"\s*:\s*\[[^\]]*?)("cta")',
            r'\1],\2',
            text,
            flags=re.S,
        )

        # Close object if missing
        if text.count("{") > text.count("}"):
            text += "}"

        return text