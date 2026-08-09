"""
Image Generation Agent

Generates actual images from approved
image prompts and registers the resulting
image assets.

Supports safe disabled mode so the main
workflow can run without making image API
requests.
"""

from config.settings import (
    IMAGE_GENERATION_ENABLED,
)

from app.image_generation_service import (
    ImageGenerationService,
)


class ImageGenerationAgent:

    def __init__(self):

        self.enabled = (
            IMAGE_GENERATION_ENABLED
        )

        self.service = None

        if self.enabled:

            self.service = (
                ImageGenerationService()
            )

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
                "Image prompts 'images' "
                "must be a list."
            )

        if not images:

            raise Exception(
                "No image prompts found."
            )

        # ------------------------------------------
        # Safe / Disabled Mode
        # ------------------------------------------

        if not self.enabled:

            print(
                "\nImage generation disabled."
            )

            print(
                "Skipping actual image generation."
            )

            return {
                "images": [],
                "enabled": False,
                "status": "skipped",
            }

        # ------------------------------------------
        # Actual Generation
        # ------------------------------------------

        generated = []

        for index, image in enumerate(
            images
        ):

            if not isinstance(
                image,
                dict
            ):

                raise Exception(
                    f"Invalid image object "
                    f"at index {index}."
                )

            scene_number = image.get(
                "scene",
                index + 1
            )

            prompt = (
                image.get("prompt")
                or image.get("image_prompt")
                or image.get("description")
            )

            if not prompt:

                raise Exception(
                    f"Missing image prompt "
                    f"for scene {scene_number}."
                )

            asset = (
                self.service.generate_scene(
                    scene_number=scene_number,
                    prompt=prompt
                )
            )

            generated.append(
                asset
            )

        return {
            "images": generated,
            "enabled": True,
            "status": "generated",
        }