"""
Workflow Engine

Runs workflow steps with
logging, saving and memory.
"""

from app.output_manager import OutputManager
from app.logger import logger


class WorkflowEngine:

    def __init__(self, memory):

        self.memory = memory

    def run_step(
        self,
        step_name,
        function,
        *args
    ):

        print(
            f"\n========== {step_name.upper()} =========="
        )

        logger.info(
            f"Starting {step_name}"
        )

        try:

            result = function(*args)

            OutputManager.save(
                step_name,
                result
            )

            self.memory.set(
                step_name,
                result
            )

            logger.info(
                f"{step_name} completed successfully"
            )

            return result

        except Exception as e:

            logger.exception(e)

            raise Exception(
                f"\n{step_name.upper()} FAILED\n\n{e}"
            )