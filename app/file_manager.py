"""
File Manager
Handles folders and files.
"""

from pathlib import Path


class FileManager:

    @staticmethod
    def create_folder(folder_name):
        Path(folder_name).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def read_text(file_path):
        """
        Read a text file and return its content.
        """
        return Path(file_path).read_text(
            encoding="utf-8"
        )