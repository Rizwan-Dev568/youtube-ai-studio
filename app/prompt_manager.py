"""
Prompt Manager

Loads prompt versions
for every AI agent.
"""

from pathlib import Path


class PromptManager:

    PROMPT_DIR = (
        Path(__file__).parent.parent
        / "agents"
        / "prompts"
    )

    def load(
        self,
        filename
    ):

        path = (
            self.PROMPT_DIR
            / filename
        )

        if not path.exists():

            raise FileNotFoundError(
                filename
            )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()