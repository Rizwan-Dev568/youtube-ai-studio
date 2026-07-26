"""
Prompt Manager

Loads prompts from text files.
"""

import os

from config.settings import PROMPTS_FOLDER


class PromptManager:

    @staticmethod
    def load(filename):

        path = os.path.join(
            PROMPTS_FOLDER,
            filename
        )

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Prompt not found: {filename}"
            )

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()