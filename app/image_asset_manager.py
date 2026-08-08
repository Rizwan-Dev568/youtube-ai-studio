"""
Image Asset Manager

Manages generated scene image metadata
without changing the existing character
AssetRegistry.
"""

import json

from pathlib import Path


class ImageAssetManager:

    STORE = (
        Path("output")
        / "image_assets.json"
    )

    def __init__(self):

        self.assets = {}

        self.load()

    def load(self):

        if not self.STORE.exists():

            self.assets = {}

            return

        try:

            with open(
                self.STORE,
                "r",
                encoding="utf-8"
            ) as file:

                self.assets = json.load(
                    file
                )

        except Exception:

            self.assets = {}

    def save(self):

        self.STORE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.STORE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.assets,
                file,
                indent=4,
                ensure_ascii=False
            )

    def register(
        self,
        scene_number,
        prompt,
        file_path,
        provider,
        model
    ):

        scene_key = str(
            int(scene_number)
        )

        self.assets[
            scene_key
        ] = {
            "scene": int(scene_number),
            "prompt": prompt,
            "file_path": str(file_path),
            "provider": provider,
            "model": model,
            "status": "generated",
        }

        self.save()

        return self.assets[
            scene_key
        ]

    def get(
        self,
        scene_number,
        default=None
    ):

        return self.assets.get(
            str(int(scene_number)),
            default
        )

    def get_all(self):

        return self.assets

    def remove(
        self,
        scene_number
    ):

        scene_key = str(
            int(scene_number)
        )

        if scene_key in self.assets:

            del self.assets[
                scene_key
            ]

            self.save()

    def clear(self):

        self.assets = {}

        self.save()