"""
Output Manager

Saves workflow results.
"""

from pathlib import Path

from app.file_manager import FileManager
from config.settings import OUTPUT_FOLDER


class OutputManager:

    @staticmethod
    def save(topic, result):

        folder_name = (
            topic
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        output_path = (
            Path(OUTPUT_FOLDER)
            / folder_name
        )

        FileManager.create_folder(output_path)

        # Complete Result
        FileManager.write_json(
            output_path / "result.json",
            result
        )

        # Individual Sections
        for key, value in result.items():

            if key == "topic":
                continue

            FileManager.write_json(
                output_path / f"{key}.json",
                value
            )