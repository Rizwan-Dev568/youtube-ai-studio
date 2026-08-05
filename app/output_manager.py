"""
Professional Output Manager
"""

import json
from pathlib import Path
from datetime import datetime

from app.logger import logger


class OutputManager:

    OUTPUT_FOLDER = Path("output")
    OUTPUT_FOLDER.mkdir(exist_ok=True)

    @staticmethod
    def save(name, data):

        try:

            file_path = OutputManager.OUTPUT_FOLDER / f"{name}.json"

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            logger.info(f"Saved: {file_path}")

            print("\n" + "=" * 60)
            print(f"SUCCESSFULLY SAVED : {file_path}")
            print("=" * 60)

        except Exception as e:

            logger.exception(e)

            raise Exception(
                f"Failed to save '{name}'.\n\n{e}"
            )

    @staticmethod
    def save_workflow(workflow):

        try:

            workflow_folder = (
                OutputManager.OUTPUT_FOLDER
                / "workflows"
            )

            workflow_folder.mkdir(exist_ok=True)

            filename = datetime.now().strftime(
                "%Y%m%d_%H%M%S.json"
            )

            file_path = workflow_folder / filename

            with open(
                file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    workflow,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            logger.info(f"Workflow Saved: {file_path}")

        except Exception as e:

            logger.exception(e)

            print(e)