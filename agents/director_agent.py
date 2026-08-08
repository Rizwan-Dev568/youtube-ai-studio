"""
Director Agent

Final AI Decision Maker

Reviews the completed pre-production workflow
and validates the Director AI response.
"""

import json

from agents.base_agent import BaseAgent
from app.output_schema import DIRECTOR_SCHEMA


class DirectorAgent(BaseAgent):

    schema = DIRECTOR_SCHEMA

    MIN_SCORE = 0
    MAX_SCORE = 100

    REQUIRED_WORKFLOW_STEPS = [
        "research",
        "seo",
        "title_rank",
        "hooks",
        "thumbnail",
        "script",
        "review",
    ]

    REQUIRED_DIRECTOR_FIELDS = [
        "overall_score",
        "approved",
        "strengths",
        "weaknesses",
        "improvements",
        "final_title",
        "final_hook",
        "final_comment",
    ]

    def __init__(self):

        super().__init__()

    def review_workflow(
        self,
        workflow
    ):

        self._validate_workflow(
            workflow
        )

        prompt = self.load_prompt(
            "director_prompt.txt"
        )

        prompt = prompt.replace(
            "{workflow}",
            json.dumps(
                workflow,
                indent=2,
                ensure_ascii=False
            )
        )

        result = self.ask(
            prompt,
            schema=self.schema
        )

        return self._validate_director_result(
            result
        )

    def _validate_workflow(
        self,
        workflow
    ):

        if not isinstance(
            workflow,
            dict
        ):
            raise Exception(
                "Director workflow must be a dictionary."
            )

        for step in self.REQUIRED_WORKFLOW_STEPS:

            if step not in workflow:

                raise Exception(
                    f"Director cannot review workflow. "
                    f"Missing step: {step}"
                )

            if workflow[step] is None:

                raise Exception(
                    f"Director workflow step is empty: {step}"
                )

    def _validate_director_result(
        self,
        result
    ):

        if not isinstance(
            result,
            dict
        ):
            raise Exception(
                "Director result must be a dictionary."
            )

        for field in self.REQUIRED_DIRECTOR_FIELDS:

            if field not in result:

                raise Exception(
                    f"Director missing required field: {field}"
                )

        score = result["overall_score"]

        if not isinstance(
            score,
            int
        ):
            raise Exception(
                "Director overall_score must be an integer."
            )

        if not (
            self.MIN_SCORE
            <= score
            <= self.MAX_SCORE
        ):
            raise Exception(
                "Director overall_score must be between "
                "0 and 100."
            )

        approved = result["approved"]

        if not isinstance(
            approved,
            bool
        ):
            raise Exception(
                "Director approved must be boolean."
            )

        if not isinstance(
            result["strengths"],
            list
        ):
            raise Exception(
                "Director strengths must be a list."
            )

        if not isinstance(
            result["weaknesses"],
            list
        ):
            raise Exception(
                "Director weaknesses must be a list."
            )

        if not isinstance(
            result["improvements"],
            list
        ):
            raise Exception(
                "Director improvements must be a list."
            )

        for field in [
            "final_title",
            "final_hook",
            "final_comment",
        ]:

            if not isinstance(
                result[field],
                str
            ):
                raise Exception(
                    f"Director {field} must be a string."
                )

            result[field] = result[field].strip()

            if not result[field]:

                raise Exception(
                    f"Director {field} cannot be empty."
                )

        self._apply_approval_gate(
            result
        )

        return result

    def _apply_approval_gate(
        self,
        result
    ):

        score = result["overall_score"]

        # Very low scores cannot be approved.
        if score < 70:

            result["approved"] = False

            if not result["improvements"]:

                result["improvements"].append(
                    "Workflow quality is below the "
                    "minimum approval threshold."
                )

        # Scores of 70+ may be approved by the AI.
        # We do not automatically approve them because
        # the Director should still make the final decision.