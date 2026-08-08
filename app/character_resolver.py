"""
Character Resolver

Resolves only the characters
required for a scene and creates
a locked prompt for AI generation.
"""

import json

from app.character_manager import CharacterManager


class CharacterResolver:

    def __init__(self):

        self.manager = CharacterManager()

    def resolve(
        self,
        scene
    ):

        if not isinstance(
            scene,
            dict
        ):

            return {}

        characters = {}

        for character_id in scene.get(
            "characters",
            []
        ):

            profile = self.manager.get(
                character_id
            )

            if profile:

                characters[
                    character_id
                ] = profile

        return characters

    def build_prompt(
        self,
        scene
    ):

        characters = self.resolve(
            scene
        )

        if not characters:

            return "No recurring characters."

        prompt = [
            "CHARACTER DATABASE",
            "",
            "Use these character profiles exactly.",
            "Never change face, hairstyle, clothing, body type or accessories.",
            ""
        ]

        for profile in characters.values():

            prompt.append(
                json.dumps(
                    profile,
                    ensure_ascii=False,
                    indent=2
                )
            )

            prompt.append("")

        return "\n".join(
            prompt
        )