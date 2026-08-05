"""
Response Parser
"""

from app.json_repair import JsonRepair


class ResponseParser:

    @staticmethod
    def parse(text):

        if text is None:
            raise Exception("AI returned None.")

        if not isinstance(text, str):
            text = str(text)

        text = text.strip()

        if not text:
            raise Exception("AI returned an empty response.")

        try:
            data = JsonRepair.loads(text)

        except Exception as e:

            print("\n" + "=" * 80)
            print("JSON PARSE FAILED")
            print("=" * 80)
            print(text)
            print("=" * 80)

            raise Exception(
                f"Failed to parse AI response.\n\n{e}"
            )

        if not isinstance(data, dict):
            raise Exception(
                "AI response is not a JSON object."
            )

        print("\n" + "=" * 80)
        print("PARSED JSON")
        print("=" * 80)
        print(data)
        print("=" * 80)

        return data