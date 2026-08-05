"""
JSON Repair Service

Uses AI to repair malformed JSON.
"""

from app.ai_client import AIClient


class JsonRepairService:

    def __init__(self):

        self.ai = AIClient()

    def repair(
        self,
        broken_json
    ):

        prompt = f"""
You are a JSON repair engine.

Repair ONLY the JSON.

Rules

- Do not rewrite content.
- Do not summarize.
- Keep every key.
- Keep every value.
- Fix syntax only.
- Return ONLY valid JSON.

Broken JSON

{broken_json}
"""

        return self.ai.ask(
            prompt,
            schema=None
        )