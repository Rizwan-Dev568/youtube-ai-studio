"""
Prompt Quality Validator

Detects malformed, corrupted, or obviously unusable
AI-generated image and video prompts.
"""


class PromptQualityValidator:

    MIN_IMAGE_PROMPT_LENGTH = 120
    MIN_VIDEO_PROMPT_LENGTH = 120

    # Words/patterns that commonly indicate corrupted
    # or malformed AI output.
    GARBAGE_PATTERNS = [
        "text_imported",
        "text imported",
        "friendly enthusiasmlease",
        "enthusiasmlease",
        "placeholder",
        "undefined",
        "nan",
        "null",
        "tasseni",
        "compos ts",
        "com posts",
    ]

    @classmethod
    def validate_images(
        cls,
        images
    ):

        if not isinstance(
            images,
            list
        ):
            raise Exception(
                "Image prompts must be a list."
            )

        if not images:

            raise Exception(
                "No image prompts were generated."
            )

        for index, image in enumerate(
            images
        ):

            if not isinstance(
                image,
                dict
            ):
                raise Exception(
                    f"Invalid image prompt at index {index}."
                )

            cls._validate_required_fields(
                image,
                [
                    "scene",
                    "title",
                    "image_prompt",
                    "negative_prompt",
                    "style",
                    "aspect_ratio",
                ],
                "image",
                index
            )

            cls._validate_text(
                image["image_prompt"],
                cls.MIN_IMAGE_PROMPT_LENGTH,
                "image_prompt",
                index
            )

            cls._validate_text(
                image["negative_prompt"],
                10,
                "negative_prompt",
                index
            )

            cls._check_garbage(
                image["image_prompt"],
                "image_prompt",
                index
            )

            cls._check_garbage(
                image["negative_prompt"],
                "negative_prompt",
                index
            )

        return True

    @classmethod
    def validate_videos(
        cls,
        videos
    ):

        if not isinstance(
            videos,
            list
        ):
            raise Exception(
                "Video prompts must be a list."
            )

        if not videos:

            raise Exception(
                "No video prompts were generated."
            )

        for index, video in enumerate(
            videos
        ):

            if not isinstance(
                video,
                dict
            ):
                raise Exception(
                    f"Invalid video prompt at index {index}."
                )

            cls._validate_required_fields(
                video,
                [
                    "scene",
                    "title",
                    "video_prompt",
                    "duration",
                    "camera_motion",
                    "transition",
                ],
                "video",
                index
            )

            cls._validate_text(
                video["video_prompt"],
                cls.MIN_VIDEO_PROMPT_LENGTH,
                "video_prompt",
                index
            )

            cls._validate_text(
                video["duration"],
                3,
                "duration",
                index
            )

            cls._validate_text(
                video["camera_motion"],
                5,
                "camera_motion",
                index
            )

            cls._validate_text(
                video["transition"],
                3,
                "transition",
                index
            )

            cls._check_garbage(
                video["video_prompt"],
                "video_prompt",
                index
            )

            cls._check_garbage(
                video["camera_motion"],
                "camera_motion",
                index
            )

            cls._check_garbage(
                video["transition"],
                "transition",
                index
            )

        return True

    @classmethod
    def _validate_required_fields(
        cls,
        data,
        fields,
        item_type,
        index
    ):

        for field in fields:

            if field not in data:

                raise Exception(
                    f"Missing key: "
                    f"{item_type}s[{index}].{field}"
                )

    @classmethod
    def _validate_text(
        cls,
        value,
        minimum_length,
        field,
        index
    ):

        if not isinstance(
            value,
            str
        ):

            raise Exception(
                f"{field} at index {index} "
                f"must be a string."
            )

        value = value.strip()

        if not value:

            raise Exception(
                f"{field} at index {index} "
                f"cannot be empty."
            )

        if len(value) < minimum_length:

            raise Exception(
                f"{field} at index {index} "
                f"is too short."
            )

    @classmethod
    def _check_garbage(
        cls,
        text,
        field,
        index
    ):

        lowered = text.lower()

        for pattern in cls.GARBAGE_PATTERNS:

            if pattern in lowered:

                raise Exception(
                    f"Corrupted text detected in "
                    f"{field} at index {index}: "
                    f"{pattern}"
                )

        # Detect unusual Unicode characters that are
        # frequently introduced into otherwise English
        # prompts by malformed model output.
        suspicious_count = 0

        for char in text:

            code = ord(char)

            if (
                code > 127
                and not cls._is_allowed_unicode(char)
            ):
                suspicious_count += 1

        if suspicious_count > 3:

            raise Exception(
                f"Suspicious corrupted characters "
                f"detected in {field} at index {index}."
            )

    @classmethod
    def _is_allowed_unicode(
        cls,
        char
    ):

        # Common punctuation and symbols that can
        # legitimately appear in prompts.
        allowed_ranges = [
            (0x00A0, 0x00FF),
            (0x2000, 0x206F),
            (0x2190, 0x21FF),
        ]

        code = ord(char)

        for start, end in allowed_ranges:

            if start <= code <= end:

                return True

        return False