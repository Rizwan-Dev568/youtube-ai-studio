"""
Character Profile Agent

Extracts consistent character profiles
from the script and scene plan.
"""

import json

from agents.base_agent import BaseAgent
from app.output_schema import CHARACTER_PROFILE_SCHEMA
from app.character_manager import CharacterManager


class CharacterProfileAgent(BaseAgent):

    schema = CHARACTER_PROFILE_SCHEMA

    def __init__(self):

        super().__init__()

        self.character_manager = CharacterManager()

    def generate(
        self,
        script,
        scene_plan
    ):

        prompt = self.load_prompt(
            "character_profile_prompt.txt"
        )

        prompt = prompt.replace(
            "{script}",
            json.dumps(
                script,
                indent=2,
                ensure_ascii=False
            )
        )

        prompt = prompt.replace(
            "{scene_plan}",
            json.dumps(
                scene_plan,
                indent=2,
                ensure_ascii=False
            )
        )

        result = self.ask(
            prompt,
            schema=self.schema
        )

        updated_characters = []

        for character in result.get(
            "characters",
            []
        ):

            character_id = (
                self.character_manager.add(
                    character
                )
            )

            character["id"] = character_id

            updated_characters.append(
                character
            )

        result["characters"] = (
            updated_characters
        )

        return result