"""
Manager Agent

Orchestrates the complete YouTube AI Studio workflow.
"""

from agents.research_agent import ResearchAgent
from agents.seo_agent import SEOAgent
from agents.title_ranker_agent import TitleRankerAgent
from agents.hook_agent import HookAgent
from agents.thumbnail_agent import ThumbnailAgent
from agents.script_writer import ScriptWriter
from agents.reviewer_agent import ReviewerAgent
from agents.director_agent import DirectorAgent
from agents.scene_planner_agent import ScenePlannerAgent
from agents.character_profile_agent import CharacterProfileAgent
from agents.image_prompt_agent import ImagePromptAgent
from agents.image_generation_agent import ImageGenerationAgent
from agents.video_prompt_agent import VideoPromptAgent
from agents.voice_prompt_agent import VoicePromptAgent

from app.output_manager import OutputManager
from app.workflow_engine import WorkflowEngine
from app.logger import logger

from memory.memory_manager import MemoryManager


class ManagerAgent:

    def __init__(self):

        self.memory = MemoryManager()

        self.workflow = WorkflowEngine(
            self.memory
        )

        self.research = ResearchAgent()
        self.seo = SEOAgent()
        self.title_ranker = TitleRankerAgent()
        self.hook = HookAgent()
        self.thumbnail = ThumbnailAgent()
        self.script = ScriptWriter()
        self.reviewer = ReviewerAgent()
        self.director = DirectorAgent()
        self.scene_planner = ScenePlannerAgent()
        self.character_profile = CharacterProfileAgent()
        self.image_prompt = ImagePromptAgent()
        self.image_generation = ImageGenerationAgent()
        self.video_prompt = VideoPromptAgent()
        self.voice_prompt = VoicePromptAgent()

    def run(
        self,
        topic
    ):

        workflow = {}

        print("\nStarting Workflow...")
        logger.info("Workflow Started")

        if self.memory.topic_exists(topic):

            print(
                "\n⚠ Topic already exists in memory."
            )

        self.memory.add_topic(topic)

        self.memory.set(
            "last_topic",
            topic
        )

        # ==========================================
        # RESEARCH
        # ==========================================

        workflow["research"] = self.workflow.run_step(
            "research",
            self.research.research,
            topic
        )

        # ==========================================
        # SEO
        # ==========================================

        workflow["seo"] = self.workflow.run_step(
            "seo",
            self.seo.generate,
            workflow["research"]
        )

        # ==========================================
        # TITLE RANKING
        # ==========================================

        workflow["title_rank"] = self.workflow.run_step(
            "title_rank",
            self.title_ranker.generate,
            workflow["seo"]["titles"]
        )

        # ==========================================
        # HOOKS
        # ==========================================

        workflow["hooks"] = self.workflow.run_step(
            "hooks",
            self.hook.generate,
            workflow["research"],
            workflow["seo"]
        )

        # ==========================================
        # THUMBNAIL
        # ==========================================

        workflow["thumbnail"] = self.workflow.run_step(
            "thumbnail",
            self.thumbnail.generate,
            workflow["research"],
            workflow["seo"]
        )

        # ==========================================
        # SCRIPT
        # ==========================================

        workflow["script"] = self.workflow.run_step(
            "script",
            self.script.write_script,
            workflow["research"],
            workflow["seo"]
        )

        # ==========================================
        # REVIEW
        # ==========================================

        workflow["review"] = self.workflow.run_step(
            "review",
            self.reviewer.review,
            workflow["research"],
            workflow["seo"],
            workflow["title_rank"],
            workflow["hooks"],
            workflow["thumbnail"],
            workflow["script"]
        )

        # ==========================================
        # DIRECTOR
        # ==========================================

        workflow["director"] = self.workflow.run_step(
            "director",
            self.director.review_workflow,
            workflow
        )

        # ==========================================
        # SCENE PLAN
        # ==========================================

        workflow["scene_plan"] = self.workflow.run_step(
            "scene_plan",
            self.scene_planner.generate,
            workflow["script"]
        )

        # ==========================================
        # CHARACTER PROFILES
        # ==========================================

        workflow["character_profiles"] = (
            self.workflow.run_step(
                "character_profiles",
                self.character_profile.generate,
                workflow["script"],
                workflow["scene_plan"]
            )
        )

        # ==========================================
        # IMAGE PROMPTS
        # ==========================================

        workflow["image_prompts"] = (
            self.workflow.run_step(
                "image_prompts",
                self.image_prompt.generate,
                workflow["scene_plan"]
            )
        )

        # ==========================================
        # IMAGE GENERATION
        # ==========================================

        workflow["image_generation"] = (
            self.workflow.run_step(
                "image_generation",
                self.image_generation.generate,
                workflow["image_prompts"]
            )
        )

        # ==========================================
        # VIDEO PROMPTS
        # ==========================================

        workflow["video_prompts"] = (
            self.workflow.run_step(
                "video_prompts",
                self.video_prompt.generate,
                workflow["image_prompts"]
            )
        )

        # ==========================================
        # VOICE PROMPT
        # ==========================================

        workflow["voice_prompt"] = (
            self.workflow.run_step(
                "voice_prompt",
                self.voice_prompt.generate,
                workflow["script"]
            )
        )

        # ==========================================
        # FINAL QUALITY GATE
        # ==========================================

        self._validate_final_workflow(
            workflow
        )

        print(
            "\n✓ Final Quality Gate Passed"
        )

        logger.info(
            "Final Quality Gate Passed"
        )

        # ==========================================
        # FINAL OUTPUT
        # ==========================================

        OutputManager.save(
            "workflow",
            workflow
        )

        OutputManager.save_workflow(
            workflow
        )

        self.memory.set(
            "last_workflow",
            workflow
        )

        self.memory.save_best_workflow(
            workflow,
            workflow["director"]["overall_score"]
        )

        logger.info(
            "Workflow Completed"
        )

        print(
            "\n===================================="
        )

        print(
            "WORKFLOW COMPLETED"
        )

        print(
            "===================================="
        )

        print(
            f"Director Score : "
            f"{workflow['director']['overall_score']}"
        )

        print(
            f"Approved : "
            f"{workflow['director']['approved']}"
        )

        print(
            f"Scenes Generated : "
            f"{len(workflow['scene_plan']['scenes'])}"
        )

        return workflow

    # ==============================================
    # FINAL WORKFLOW VALIDATION
    # ==============================================

    def _validate_final_workflow(
        self,
        workflow
    ):

        required_steps = [
            "research",
            "seo",
            "title_rank",
            "hooks",
            "thumbnail",
            "script",
            "review",
            "director",
            "scene_plan",
            "character_profiles",
            "image_prompts",
            "image_generation",
            "video_prompts",
            "voice_prompt",
        ]

        # ------------------------------------------
        # Required workflow steps
        # ------------------------------------------

        for step in required_steps:

            if step not in workflow:

                raise Exception(
                    f"Final validation failed. "
                    f"Missing workflow step: {step}"
                )

            if workflow[step] is None:

                raise Exception(
                    f"Final validation failed. "
                    f"Empty workflow step: {step}"
                )

        # ------------------------------------------
        # Director approval
        # ------------------------------------------

        director = workflow["director"]

        if not isinstance(
            director,
            dict
        ):

            raise Exception(
                "Final validation failed. "
                "Director output is invalid."
            )

        if director.get(
            "approved"
        ) is not True:

            raise Exception(
                "Final validation failed. "
                "Director did not approve the workflow."
            )

        # ------------------------------------------
        # Scene plan
        # ------------------------------------------

        scene_plan = workflow["scene_plan"]

        scenes = scene_plan.get(
            "scenes",
            []
        )

        if not isinstance(
            scenes,
            list
        ):

            raise Exception(
                "Final validation failed. "
                "Scene plan must contain a list."
            )

        if not scenes:

            raise Exception(
                "Final validation failed. "
                "No scenes were generated."
            )

        scene_count = len(
            scenes
        )

        # ------------------------------------------
        # Character profiles
        # ------------------------------------------

        character_profiles = (
            workflow["character_profiles"]
        )

        characters = character_profiles.get(
            "characters",
            []
        )

        if not isinstance(
            characters,
            list
        ):

            raise Exception(
                "Final validation failed. "
                "Character profiles must contain a list."
            )

        # ------------------------------------------
        # Image prompts
        # ------------------------------------------

        image_prompts = (
            workflow["image_prompts"]
        )

        images = image_prompts.get(
            "images",
            []
        )

        if not isinstance(
            images,
            list
        ):

            raise Exception(
                "Final validation failed. "
                "Image prompts must contain a list."
            )

        if len(images) != scene_count:

            raise Exception(
                "Final validation failed. "
                f"Scene count = {scene_count}, "
                f"but image count = {len(images)}."
            )

        # ------------------------------------------
        # Image generation
        # ------------------------------------------

        image_generation = (
            workflow["image_generation"]
        )

        if not isinstance(
            image_generation,
            dict
        ):

            raise Exception(
                "Final validation failed. "
                "Image generation output is invalid."
            )

        generation_status = (
            image_generation.get(
                "status"
            )
        )

        if generation_status not in (
            "skipped",
            "generated",
        ):

            raise Exception(
                "Final validation failed. "
                "Invalid image generation status: "
                f"{generation_status}"
            )

        generated_images = (
            image_generation.get(
                "images",
                []
            )
        )

        if not isinstance(
            generated_images,
            list
        ):

            raise Exception(
                "Final validation failed. "
                "Generated images must contain a list."
            )

        # ------------------------------------------
        # Video prompts
        # ------------------------------------------

        video_prompts = (
            workflow["video_prompts"]
        )

        videos = video_prompts.get(
            "videos",
            []
        )

        if not isinstance(
            videos,
            list
        ):

            raise Exception(
                "Final validation failed. "
                "Video prompts must contain a list."
            )

        if len(videos) != scene_count:

            raise Exception(
                "Final validation failed. "
                f"Scene count = {scene_count}, "
                f"but video count = {len(videos)}."
            )

        # ------------------------------------------
        # Scene numbering
        # ------------------------------------------

        expected_numbers = list(
            range(
                1,
                scene_count + 1
            )
        )

        scene_numbers = []

        for scene in scenes:

            if not isinstance(
                scene,
                dict
            ):

                raise Exception(
                    "Final validation failed. "
                    "Invalid scene object."
                )

            number = scene.get(
                "scene"
            )

            if isinstance(
                number,
                int
            ):

                scene_numbers.append(
                    number
                )

        image_numbers = []

        for image in images:

            if not isinstance(
                image,
                dict
            ):

                raise Exception(
                    "Final validation failed. "
                    "Invalid image prompt object."
                )

            number = image.get(
                "scene"
            )

            if isinstance(
                number,
                int
            ):

                image_numbers.append(
                    number
                )

        video_numbers = []

        for video in videos:

            if not isinstance(
                video,
                dict
            ):

                raise Exception(
                    "Final validation failed. "
                    "Invalid video prompt object."
                )

            number = video.get(
                "scene"
            )

            if isinstance(
                number,
                int
            ):

                video_numbers.append(
                    number
                )

        if scene_numbers != expected_numbers:

            raise Exception(
                "Final validation failed. "
                f"Scene numbers are invalid: "
                f"{scene_numbers}"
            )

        if image_numbers != expected_numbers:

            raise Exception(
                "Final validation failed. "
                f"Image scene numbers are invalid: "
                f"{image_numbers}"
            )

        if video_numbers != expected_numbers:

            raise Exception(
                "Final validation failed. "
                f"Video scene numbers are invalid: "
                f"{video_numbers}"
            )

        # ------------------------------------------
        # Voice prompt
        # ------------------------------------------

        voice_output = (
            workflow["voice_prompt"]
        )

        if not isinstance(
            voice_output,
            dict
        ):

            raise Exception(
                "Final validation failed. "
                "Voice output is invalid."
            )

        voice = voice_output.get(
            "voice"
        )

        if not isinstance(
            voice,
            dict
        ):

            raise Exception(
                "Final validation failed. "
                "Voice object is missing."
            )

        voice_prompt = voice.get(
            "voice_prompt"
        )

        if not isinstance(
            voice_prompt,
            str
        ):

            raise Exception(
                "Final validation failed. "
                "Voice prompt is invalid."
            )

        if not voice_prompt.strip():

            raise Exception(
                "Final validation failed. "
                "Voice prompt is empty."
            )

        # ------------------------------------------
        # Final success
        # ------------------------------------------

        logger.info(
            "Final workflow validation successful"
        )

        return True