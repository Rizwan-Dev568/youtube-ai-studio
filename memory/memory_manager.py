"""
Memory Manager

Stores long-term project memory for all AI agents.
"""

import json
from pathlib import Path


class MemoryManager:

    def __init__(self):

        self.memory_folder = Path("memory")

        self.memory_folder.mkdir(
            exist_ok=True
        )

    def _file(self, name):

        return self.memory_folder / f"{name}.json"

    def load(self, name):

        file = self._file(name)

        if not file.exists():

            return []

        try:

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return []

    def save(self, name, data):

        file = self._file(name)

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )

    def add(self, name, item):

        data = self.load(name)

        if item not in data:

            data.append(item)

            self.save(
                name,
                data
            )

    def clear(self, name):

        self.save(
            name,
            []
        )