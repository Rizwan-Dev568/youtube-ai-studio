"""
Workflow Engine

Runs workflow steps with
logging, saving and memory.
Supports automatic resume.
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
        *args,
        force=False
    ):

        print(
            f"\n========== {step_name.upper()} =========="
        )

        logger.info(
            f"Starting {step_name}"
        )

        # -----------------------------
        # Resume Mode
        # -----------------------------
        if not force:

            cached = self.memory.get(
                step_name
            )

            if cached is not None:

                print(
                    f"✓ Resuming '{step_name}' from memory."
                )

                logger.info(
                    f"{step_name} loaded from memory."
                )

                return cached

        try:

            result = function(
                *args
            )

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