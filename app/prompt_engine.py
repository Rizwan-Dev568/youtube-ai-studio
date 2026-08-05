"""
Prompt Engine

Loads prompts and replaces variables.
"""

from pathlib import Path


class PromptEngine:

    PROMPT_FOLDER = (
        Path(__file__).parent.parent
        / "agents"
        / "prompts"
    )

    @classmethod
    def render(
        cls,
        filename,
        **kwargs
    ):

        prompt_file = (
            cls.PROMPT_FOLDER
            / filename
        )

        with open(
            prompt_file,
            "r",
            encoding="utf-8"
        ) as f:

            prompt = f.read()

        for key, value in kwargs.items():

            prompt = prompt.replace(
                "{" + key + "}",
                str(value)
            )

        return prompt