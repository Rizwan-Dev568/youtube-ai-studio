"""
Image Generator

Provider-independent image generation layer.

Routes image generation requests to
the configured image provider.
"""

from config.settings import IMAGE_PROVIDER

from app.gemini_image_client import GeminiImageClient


class ImageGenerator:

    def __init__(self):

        self.provider = (
            IMAGE_PROVIDER
            .lower()
            .strip()
        )

        self.client = self._create_client()

    def _create_client(self):

        if self.provider == "gemini":

            return GeminiImageClient()

        raise ValueError(
            f"Unsupported image provider: "
            f"{IMAGE_PROVIDER}"
        )

    def generate(
        self,
        prompt,
        scene_number=None,
        filename=None,
        aspect_ratio=None
    ):

        if not prompt:

            raise ValueError(
                "Image prompt cannot be empty."
            )

        return self.client.generate(
            prompt=prompt,
            scene_number=scene_number,
            filename=filename,
            aspect_ratio=aspect_ratio
        )