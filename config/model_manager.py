"""
Model Manager

Keeps track of working and disabled models.
"""

import json
from pathlib import Path

from config.ai_models import OPENROUTER_MODELS


class ModelManager:

    CACHE_FILE = (
        Path(__file__).parent
        / "model_cache.json"
    )

    def __init__(self):

        self.models = list(
            OPENROUTER_MODELS
        )

        self.disabled = []

        self.load()

    def load(self):

        if not self.CACHE_FILE.exists():
            return

        try:

            with open(
                self.CACHE_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                data = json.load(f)

            self.disabled = data.get(
                "disabled_models",
                []
            )

            self.models = [
                model
                for model in OPENROUTER_MODELS
                if model not in self.disabled
            ]

        except Exception:

            self.models = list(
                OPENROUTER_MODELS
            )

            self.disabled = []

    def save(self):

        with open(
            self.CACHE_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                {
                    "working_models": self.models,
                    "disabled_models": self.disabled,
                },
                f,
                indent=4,
                ensure_ascii=False,
            )

    def get_models(self):

        return self.models

    def remove_model(
        self,
        model
    ):

        if model in self.models:

            self.models.remove(model)

        if model not in self.disabled:

            self.disabled.append(model)

        self.save()

    def reset(self):

        self.models = list(
            OPENROUTER_MODELS
        )

        self.disabled = []

        self.save()

    def has_models(self):

        return len(self.models) > 0