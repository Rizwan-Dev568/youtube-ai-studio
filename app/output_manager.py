"""
Output Manager

Automatically saves every agent output.
"""

import json
from pathlib import Path


class OutputManager:

    OUTPUT_FOLDER = Path("output")

    @staticmethod
    def save(name, data):

        OutputManager.OUTPUT_FOLDER.mkdir(
            exist_ok=True
        )

        file = (
            OutputManager.OUTPUT_FOLDER
            / f"{name}.json"
        )

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(
            f"\n✅ Saved: {file}"
        )