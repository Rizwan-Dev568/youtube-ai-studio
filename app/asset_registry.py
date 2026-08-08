"""
Asset Registry

Stores reusable production assets
for characters.
"""

import json

from pathlib import Path


class AssetRegistry:

    STORE = (
        Path(__file__).parent
        / "assets.json"
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
            ) as f:

                self.assets = json.load(f)

        except Exception:

            self.assets = {}

    def save(self):

        with open(
            self.STORE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.assets,
                f,
                indent=4,
                ensure_ascii=False
            )

    def set_asset(
        self,
        character_id,
        asset_name,
        value
    ):

        if character_id not in self.assets:

            self.assets[
                character_id
            ] = {}

        self.assets[
            character_id
        ][asset_name] = value

        self.save()

    def get_asset(
        self,
        character_id,
        asset_name,
        default=None
    ):

        return (
            self.assets
            .get(character_id, {})
            .get(asset_name, default)
        )

    def get_assets(
        self,
        character_id
    ):

        return self.assets.get(
            character_id,
            {}
        )

    def clear(self):

        self.assets = {}

        self.save()