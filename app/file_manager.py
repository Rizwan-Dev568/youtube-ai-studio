"""
File Manager
Handles folders and files.
"""

from pathlib import Path


class FileManager:

    @staticmethod
    def create_folder(folder_name):
        Path(folder_name).mkdir(parents=True, exist_ok=True)