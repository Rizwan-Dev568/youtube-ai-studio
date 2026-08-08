"""
Image Prompt Agent

Generates professional AI image prompts
for every planned scene with strict
character consistency and quality validation.
"""

import json

from agents.base_agent import BaseAgent
from app.output_schema import IMAGE_PROMPT_SCHEMA
from app.character_resolver import CharacterResolver
from app.prompt_quality_validator import PromptQualityValidator


class ImagePromptAgent(BaseAgent):

    schema = IMAGE_PROMPT_SCHEMA

    def __init__(self):

        super().__init__()

        self.character_resolver = CharacterResolver()
        self.quality_validator = PromptQualityValidator()

    def generate(
        self,
        scene_plan
    ):

        if not isinstance(
            scene_plan,
            dict
        ):
            raise Exception(
                "Scene plan must be a dictionary."
            )

        scenes = scene_plan.get(
            "scenes",
            []
        )

        if not isinstance(
            scenes,
            list
        ):
            raise Exception(
                "Scene plan 'scenes' must be a list."
            )

        if not scenes:

            raise Exception(
                "No scenes found in scene plan."
            )

        resolved_scenes = []

        for scene in scenes:

            if not isinstance(
                scene,
                dict
            ):
                raise Exception(
                    "Invalid scene found in scene plan."
                )

            character_ids = scene.get(
                "characters",
                []
            )

            characters = (
                self.character_resolver.resolve(
                    scene
                )
            )

            resolved_scenes.append(
                {
                    "scene": scene,
                    "character_ids": character_ids,
                    "characters": characters,
                }
            )

        if len(resolved_scenes) != len(scenes):

            raise Exception(
                "Some scenes could not be resolved."
            )

        prompt = self.load_prompt(
            "image_prompt.txt"
        )

        character_data = json.dumps(
            resolved_scenes,
            indent=2,
            ensure_ascii=False
        )

        prompt = prompt.replace(
            "{characters}",
            character_data
        )

        prompt = prompt.replace(
            "{scene_plan}",
            character_data
        )

        # Quality validation is now handled inside
        # BaseAgent.ask(), which allows automatic
        # retry when corrupted prompts are detected.

        result = self.ask(
            prompt,
            schema=self.schema,
            quality_validator=self.quality_validator,
            quality_type="images"
        )

        # Enforce correct scene numbering after
        # successful quality validation.

        result = self._enforce_scene_numbers(
            result,
            len(resolved_scenes)
        )

        print(
            "\n✓ Image Prompt Quality Passed"
        )

        return result

    def _enforce_scene_numbers(
        self,
        result,
        scene_count
    ):

        if not isinstance(
            result,
            dict
        ):
            raise Exception(
                "Image prompt result must be an object."
            )

        images = result.get(
            "images",
            []
        )

        if not isinstance(
            images,
            list
        ):
            raise Exception(
                "Image prompt 'images' must be a list."
            )

        if len(images) != scene_count:

            raise Exception(
                f"Expected {scene_count} image prompts, "
                f"but AI returned {len(images)}."
            )

        for index, image in enumerate(
            images
        ):

            if not isinstance(
                image,
                dict
            ):
                raise Exception(
                    f"Invalid image object at index {index}."
                )

            image["scene"] = index + 1

        return result