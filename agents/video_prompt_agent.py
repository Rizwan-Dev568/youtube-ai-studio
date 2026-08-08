"""
Video Prompt Agent

Generates cinematic AI video prompts
for every image prompt with quality validation
and automatic retry support.
"""

import json

from agents.base_agent import BaseAgent
from app.output_schema import VIDEO_PROMPT_SCHEMA
from app.prompt_quality_validator import PromptQualityValidator


class VideoPromptAgent(BaseAgent):

    schema = VIDEO_PROMPT_SCHEMA

    def __init__(self):

        super().__init__()

        self.quality_validator = PromptQualityValidator()

    def generate(
        self,
        image_prompts
    ):

        if not isinstance(
            image_prompts,
            dict
        ):
            raise Exception(
                "Image prompts must be a dictionary."
            )

        images = image_prompts.get(
            "images",
            []
        )

        if not isinstance(
            images,
            list
        ):
            raise Exception(
                "Image prompts 'images' must be a list."
            )

        if not images:

            raise Exception(
                "No image prompts found."
            )

        prompt = self.load_prompt(
            "video_prompt.txt"
        )

        prompt = prompt.replace(
            "{image_prompts}",
            json.dumps(
                image_prompts,
                indent=2,
                ensure_ascii=False
            )
        )

        # Quality validation is handled inside
        # BaseAgent.ask(), allowing automatic retry
        # when corrupted video prompts are detected.

        result = self.ask(
            prompt,
            schema=self.schema,
            quality_validator=self.quality_validator,
            quality_type="videos"
        )

        # Enforce correct scene numbering only
        # after the AI response passes validation.

        result = self._enforce_scene_numbers(
            result,
            len(images)
        )

        print(
            "\n✓ Video Prompt Quality Passed"
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
                "Video prompt result must be a dictionary."
            )

        videos = result.get(
            "videos",
            []
        )

        if not isinstance(
            videos,
            list
        ):
            raise Exception(
                "Video prompt 'videos' must be a list."
            )

        if len(videos) != scene_count:

            raise Exception(
                f"Expected {scene_count} video prompts, "
                f"but AI returned {len(videos)}."
            )

        for index, video in enumerate(
            videos
        ):

            if not isinstance(
                video,
                dict
            ):
                raise Exception(
                    f"Invalid video object at index {index}."
                )

            video["scene"] = index + 1

        return result