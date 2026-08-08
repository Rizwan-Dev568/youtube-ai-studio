"""
Image Generation Service

Coordinates image generation and
scene image asset registration.
"""

from app.image_generator import ImageGenerator
from app.image_asset_manager import ImageAssetManager


class ImageGenerationService:

    def __init__(self):

        self.generator = ImageGenerator()

        self.assets = ImageAssetManager()

    def generate_scene(
        self,
        scene_number,
        prompt,
        filename=None,
        aspect_ratio=None
    ):

        if scene_number is None:

            raise ValueError(
                "Scene number is required."
            )

        if not prompt:

            raise ValueError(
                "Image prompt is required."
            )

        file_path = self.generator.generate(
            prompt=prompt,
            scene_number=scene_number,
            filename=filename,
            aspect_ratio=aspect_ratio
        )

        asset = self.assets.register(
            scene_number=scene_number,
            prompt=prompt,
            file_path=file_path,
            provider=self.generator.provider,
            model=self.generator.client.model
        )

        return asset