"""
Workflow Engine

Runs workflow steps with
logging, saving and memory.

Supports automatic resume with
topic-aware workflow memory.
"""

import hashlib

from app.output_manager import OutputManager
from app.logger import logger


class WorkflowEngine:

    def __init__(self, memory):

        self.memory = memory
        self.topic = None

    # --------------------------------------------------
    # Workflow Context
    # --------------------------------------------------

    def set_topic(self, topic):

        if not topic:

            raise ValueError(
                "Workflow topic cannot be empty."
            )

        if not isinstance(
            topic,
            str
        ):

            raise TypeError(
                "Workflow topic must be a string."
            )

        topic = topic.strip()

        if not topic:

            raise ValueError(
                "Workflow topic cannot be empty."
            )

        self.topic = topic

    # --------------------------------------------------
    # Topic Memory Key
    # --------------------------------------------------

    def _memory_key(
        self,
        step_name
    ):

        if not self.topic:

            raise RuntimeError(
                "Workflow topic is not set. "
                "Call set_topic() before run_step()."
            )

        topic_hash = hashlib.sha256(
            self.topic.lower().encode(
                "utf-8"
            )
        ).hexdigest()[:16]

        return (
            f"workflow:"
            f"{topic_hash}:"
            f"{step_name}"
        )

    # --------------------------------------------------
    # Run Step
    # --------------------------------------------------

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

        memory_key = self._memory_key(
            step_name
        )

        # -----------------------------
        # Resume Mode
        # -----------------------------

        if not force:

            cached = self.memory.get(
                memory_key
            )

            if cached is not None:

                print(
                    f"✓ Resuming '{step_name}' "
                    f"from memory."
                )

                logger.info(
                    f"{step_name} loaded from "
                    "topic memory."
                )

                return cached

        # -----------------------------
        # Execute Step
        # -----------------------------

        try:

            result = function(
                *args
            )

            OutputManager.save(
                step_name,
                result
            )

            self.memory.set(
                memory_key,
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