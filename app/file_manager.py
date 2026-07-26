"""
File Manager

Handles reading and writing files.
"""

import json
from pathlib import Path


class FileManager:

    @staticmethod
    def create_folder(folder_path):
        """
        Create folder if it doesn't exist.
        """
        Path(folder_path).mkdir(
            parents=True,
            exist_ok=True
        )

    @staticmethod
    def read_text(file_path):
        """
        Read text file.
        """
        return Path(file_path).read_text(
            encoding="utf-8"
        )

    @staticmethod
    def write_text(file_path, content):
        """
        Write text file.
        """
        file_path = Path(file_path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

    @staticmethod
    def write_json(file_path, data):
        """
        Save dictionary as JSON.
        """
        file_path = Path(file_path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    @staticmethod
    def read_json(file_path):
        """
        Read JSON file.
        """
        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    @staticmethod
    def file_exists(file_path):
        """
        Check if file exists.
        """
        return Path(file_path).exists()

    @staticmethod
    def delete_file(file_path):
        """
        Delete a file if it exists.
        """
        file_path = Path(file_path)

        if file_path.exists():
            file_path.unlink()