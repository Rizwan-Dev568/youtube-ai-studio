"""
Voice Prompt Agent

Generates professional AI voice prompts
with strict output validation.
"""

import json

from agents.base_agent import BaseAgent
from app.output_schema import VOICE_PROMPT_SCHEMA


class VoicePromptAgent(BaseAgent):

    schema = VOICE_PROMPT_SCHEMA

    REQUIRED_FIELDS = [
        "language",
        "gender",
        "age",
        "accent",
        "pace",
        "style",
        "emotion",
        "energy",
        "pronunciation_notes",
        "pause_instructions",
        "voice_prompt",
    ]

    def __init__(self):

        super().__init__()

    def generate(
        self,
        script
    ):

        if not isinstance(
            script,
            dict
        ):
            raise Exception(
                "Script must be a dictionary."
            )

        prompt = self.load_prompt(
            "voice_prompt.txt"
        )

        prompt = prompt.replace(
            "{script}",
            json.dumps(
                script,
                indent=2,
                ensure_ascii=False
            )
        )

        result = self.ask(
            prompt,
            schema=self.schema
        )

        return self._validate_voice_output(
            result
        )

    def _validate_voice_output(
        self,
        result
    ):

        if not isinstance(
            result,
            dict
        ):
            raise Exception(
                "Voice prompt result must be a dictionary."
            )

        voice = result.get(
            "voice"
        )

        if not isinstance(
            voice,
            dict
        ):
            raise Exception(
                "Voice output must contain a 'voice' object."
            )

        for field in self.REQUIRED_FIELDS:

            if field not in voice:

                raise Exception(
                    f"Missing voice field: {field}"
                )

            value = voice[field]

            if not isinstance(
                value,
                str
            ):
                raise Exception(
                    f"Voice field '{field}' must be a string."
                )

            voice[field] = value.strip()

            if not voice[field]:

                raise Exception(
                    f"Voice field '{field}' cannot be empty."
                )

        self._check_garbage(
            voice["voice_prompt"]
        )

        return result

    def _check_garbage(
        self,
        text
    ):

        garbage_patterns = [
            "friendly enthusiasmlease",
            "enthusiasmlease",
            "placeholder",
            "undefined",
            "null",
            "nan",
            "todo",
        ]

        lowered = text.lower()

        for pattern in garbage_patterns:

            if pattern in lowered:

                raise Exception(
                    "Invalid or corrupted voice prompt detected: "
                    f"{pattern}"
                )

        if len(text) < 20:

            raise Exception(
                "Voice prompt is too short."
            )