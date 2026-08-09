"""
Gemini Image Client

Handles image generation through
Google Gemini image generation models.
"""

from pathlib import Path

from google import genai
from google.genai import types
from google.genai import errors

from config.settings import (
    GEMINI_API_KEY,
    IMAGE_GENERATION_MODEL,
    DEFAULT_ASPECT_RATIO,
    IMAGE_OUTPUT_FOLDER,
)

from app.logger import logger


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

        logger.info(
            "Gemini image generation started | "
            f"model={self.model} | "
            f"scene={scene_number}"
        )

        try:

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

        except errors.ClientError as e:

            message = str(e)

            if "429" in message or (
                "RESOURCE_EXHAUSTED"
                in message
            ):

                logger.error(
                    "Gemini image generation "
                    "quota exceeded."
                )

                raise RuntimeError(
                    "Gemini image generation "
                    "quota exceeded. "
                    "Check your Gemini API "
                    "plan, billing, and quota."
                ) from e

            if "401" in message or (
                "403" in message
            ):

                logger.error(
                    "Gemini image API "
                    "authentication/permission error."
                )

                raise RuntimeError(
                    "Gemini image API "
                    "authentication or "
                    "permission error. "
                    "Check GEMINI_API_KEY "
                    "and API access."
                ) from e

            if "404" in message or (
                "NOT_FOUND"
                in message
            ):

                logger.error(
                    "Gemini image model "
                    f"not available: {self.model}"
                )

                raise RuntimeError(
                    "Gemini image model is "
                    f"not available: {self.model}. "
                    "Check IMAGE_GENERATION_MODEL."
                ) from e

            logger.error(
                "Gemini client error: "
                f"{message}"
            )

            raise RuntimeError(
                "Gemini image generation "
                "client error: "
                f"{message}"
            ) from e

        except errors.ServerError as e:

            logger.error(
                "Gemini server error: "
                f"{e}"
            )

            raise RuntimeError(
                "Gemini image generation "
                "server error. "
                "Please try again later."
            ) from e

        except errors.APIError as e:

            logger.error(
                "Gemini API error: "
                f"{e}"
            )

            raise RuntimeError(
                "Gemini image generation "
                "API error: "
                f"{e}"
            ) from e

        except Exception as e:

            logger.exception(
                "Unexpected Gemini image "
                "generation error."
            )

            raise RuntimeError(
                "Unexpected error during "
                "Gemini image generation: "
                f"{e}"
            ) from e

        if response is None:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        image_data = self._extract_image(
            response
        )

        if image_data is None:

            raise RuntimeError(
                "Gemini response did not contain "
                "image data."
            )

        output_path = self._build_output_path(
            scene_number=scene_number,
            filename=filename
        )

        try:

            output_path.write_bytes(
                image_data
            )

        except Exception as e:

            logger.exception(
                "Failed to save generated "
                f"image: {output_path}"
            )

            raise RuntimeError(
                "Failed to save generated "
                f"image to {output_path}: {e}"
            ) from e

        logger.info(
            "Gemini image generated successfully | "
            f"scene={scene_number} | "
            f"path={output_path}"
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