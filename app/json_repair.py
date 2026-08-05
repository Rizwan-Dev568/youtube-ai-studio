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
            text = str(text)

        text = text.strip()

        # Remove markdown
        text = re.sub(r"^```json\s*", "", text, flags=re.I)
        text = re.sub(r"^```\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

        # Keep only JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            text = text[start:end + 1]

        # Normalize quotes
        text = (
            text.replace("“", '"')
                .replace("”", '"')
                .replace("‘", "'")
                .replace("’", "'")
        )

        # Remove control characters
        text = re.sub(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F]",
            "",
            text
        )

        # Remove trailing commas
        text = re.sub(
            r",(\s*[}\]])",
            r"\1",
            text
        )

        # ---------- Common AI Fixes ----------

        # CTA accidentally inside sections
        text = re.sub(
            r'"CTA"\s*:',
            '"cta":',
            text
        )

        # Double commas
        text = re.sub(
            r",\s*,",
            ",",
            text
        )

        # Missing comma between ] and next key
        text = re.sub(
            r'"\]\s*"',
            '"],"',
            text
        )

        return text.strip()

    @staticmethod
    def second_pass(text):

        # Remove trailing commas
        text = re.sub(
            r",(\s*[}\]])",
            r"\1",
            text
        )

        # Balance braces
        while text.count("{") > text.count("}"):
            text += "}"

        while text.count("[") > text.count("]"):
            text += "]"

        return text

    @staticmethod
    def loads(text):

        repaired = JsonRepair.repair(text)

        print("\n" + "=" * 80)
        print("JSON AFTER REPAIR")
        print("=" * 80)
        print(repaired)
        print("=" * 80)

        try:

            return json.loads(repaired)

        except Exception as first_error:

            print("\nFirst Parse Failed")
            print(first_error)

            repaired = JsonRepair.second_pass(
                repaired
            )

            print("\n" + "=" * 80)
            print("SECOND PASS JSON")
            print("=" * 80)
            print(repaired)
            print("=" * 80)

            try:

                return json.loads(repaired)

            except Exception:

                # ---------- Last Chance AI Fix ----------

                try:

                    # Remove malformed CTA inside sections
                    repaired = re.sub(
                        r',"cta"\s*:\s*".*?"\s*\]',
                        '"]',
                        repaired,
                        flags=re.S
                    )

                    repaired = JsonRepair.second_pass(
                        repaired
                    )

                    print("\n" + "=" * 80)
                    print("LAST CHANCE REPAIR")
                    print("=" * 80)
                    print(repaired)
                    print("=" * 80)

                    return json.loads(repaired)

                except Exception as last_error:

                    print("\nJSON PARSE FAILED")
                    print(last_error)

                    raise Exception(
                        f"\nInvalid JSON returned by AI.\n\n{last_error}"
                    )