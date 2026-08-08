"""
Character Manager

Stores reusable character profiles
for the entire workflow.
"""

import json
import uuid
from app.asset_registry import AssetRegistry
from pathlib import Path


class CharacterManager:

    STORE = (
        Path(__file__).parent
        / "characters.json"
    )

    def __init__(self):

       self.characters = {}

       self.assets = AssetRegistry()

       self.load()

    def load(self):

        if not self.STORE.exists():
            return

        try:

            with open(
                self.STORE,
                "r",
                encoding="utf-8"
            ) as f:

                self.characters = json.load(f)

        except Exception:

            self.characters = {}

    def save(self):

        with open(
            self.STORE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.characters,
                f,
                indent=4,
                ensure_ascii=False
            )

    def create_id(self):

        return (
            "char_"
            + uuid.uuid4().hex[:8]
        )

    def find_by_name(
        self,
        name
    ):

        if not name:
            return None

        target = name.strip().lower()

        for character_id, profile in self.characters.items():

            profile_name = (
                profile.get("name", "")
                .strip()
                .lower()
            )

            if profile_name == target:

                return character_id

        return None

    def add(
        self,
        profile
    ):

        name = profile.get(
            "name"
        )

        existing = self.find_by_name(
            name
        )

        if existing:

            profile["id"] = existing

            self.characters[
                existing
            ] = profile

            self.save()

            return existing

        character_id = self.create_id()

        profile["id"] = character_id

        self.characters[
            character_id
        ] = profile

        self.assets.set_asset(
            character_id,
            "profile_created",
            True
        )

        self.save()

        return character_id

    def get(
        self,
        character_id,
        default=None
    ):

        return self.characters.get(
            character_id,
            default
        )

    def all(self):

        return self.characters

    def clear(self):

        self.characters = {}

        self.save()