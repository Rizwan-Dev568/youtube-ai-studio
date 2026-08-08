"""
Gemini Image Client

Handles image generation through
Google Gemini image generation models.
"""

from pathlib import Path

from google import genai
from google.genai import types

from config.settings import (
    GEMINI_API_KEY,
    IMAGE_GENERATION_MODEL,
    DEFAULT_ASPECT_RATIO,
    IMAGE_OUTPUT_FOLDER,
)


class GeminiImageClient:

    def __init__(self):

        if not GEMINI_API_KEY:

            raise ValueError(
                "GEMINI_API_KEY is missing."
            )

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = IMAGE_GENERATION_MODEL

        self.output_folder = Path(
            IMAGE_OUTPUT_FOLDER
        )

        self.output_folder.mkdir(
            parents=True,
            exist_ok=True
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

        if not isinstance(
            prompt,
            str
        ):

            raise TypeError(
                "Image prompt must be a string."
            )

        aspect_ratio = (
            aspect_ratio
            or DEFAULT_ASPECT_RATIO
        )

        response = (
            self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=[
                        "TEXT",
                        "IMAGE"
                    ],
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio
                    )
                )
            )
        )

        if response is None:

            raise Exception(
                "Gemini returned an empty response."
            )

        image_data = self._extract_image(
            response
        )

        if image_data is None:

            raise Exception(
                "Gemini response did not contain "
                "image data."
            )

        output_path = self._build_output_path(
            scene_number=scene_number,
            filename=filename
        )

        output_path.write_bytes(
            image_data
        )

        return str(
            output_path
        )

    def _extract_image(
        self,
        response
    ):

        candidates = getattr(
            response,
            "candidates",
            None
        )

        if not candidates:

            return None

        for candidate in candidates:

            content = getattr(
                candidate,
                "content",
                None
            )

            if content is None:

                continue

            parts = getattr(
                content,
                "parts",
                []
            )

            for part in parts:

                inline_data = getattr(
                    part,
                    "inline_data",
                    None
                )

                if inline_data is None:

                    continue

                data = getattr(
                    inline_data,
                    "data",
                    None
                )

                if data is not None:

                    return data

        return None

    def _build_output_path(
        self,
        scene_number=None,
        filename=None
    ):

        if filename:

            safe_name = Path(
                filename
            ).name

            if not safe_name.lower().endswith(
                ".png"
            ):

                safe_name += ".png"

            return (
                self.output_folder
                / safe_name
            )

        if scene_number is not None:

            return (
                self.output_folder
                / f"scene_{int(scene_number):03d}.png"
            )

        return (
            self.output_folder
            / "generated_image.png"
        )