from agents.research_agent import ResearchAgent
from agents.seo_agent import SEOAgent
from agents.title_ranker_agent import TitleRankerAgent
from agents.hook_agent import HookAgent
from agents.thumbnail_agent import ThumbnailAgent
from agents.script_writer import ScriptWriter
from agents.reviewer_agent import ReviewerAgent
from agents.director_agent import DirectorAgent
from agents.scene_planner_agent import ScenePlannerAgent

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

    def run(self, topic):

        workflow = {}

        print("\nStarting Workflow...")
        logger.info("Workflow Started")

        if self.memory.topic_exists(topic):

            print("\n⚠ Topic already exists in memory.")

        self.memory.add_topic(topic)
        self.memory.set("last_topic", topic)

        workflow["research"] = self.workflow.run_step(
            "research",
            self.research.research,
            topic
        )

        workflow["seo"] = self.workflow.run_step(
            "seo",
            self.seo.generate,
            workflow["research"]
        )

        workflow["title_rank"] = self.workflow.run_step(
            "title_rank",
            self.title_ranker.generate,
            workflow["seo"]["titles"]
        )

        workflow["hooks"] = self.workflow.run_step(
            "hooks",
            self.hook.generate,
            workflow["research"],
            workflow["seo"]
        )

        workflow["thumbnail"] = self.workflow.run_step(
            "thumbnail",
            self.thumbnail.generate,
            workflow["research"],
            workflow["seo"]
        )

        workflow["script"] = self.workflow.run_step(
            "script",
            self.script.write_script,
            workflow["research"],
            workflow["seo"]
        )

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

        workflow["director"] = self.workflow.run_step(
            "director",
            self.director.review_workflow,
            workflow
        )

        workflow["scene_plan"] = self.workflow.run_step(
            "scene_plan",
            self.scene_planner.generate,
            workflow["script"]
        )

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

        logger.info("Workflow Completed")

        print("\n====================================")
        print("WORKFLOW COMPLETED")
        print("====================================")

        print(
            f"Director Score : {workflow['director']['overall_score']}"
        )

        print(
            f"Approved : {workflow['director']['approved']}"
        )

        print(
            f"Scenes Generated : {len(workflow['scene_plan']['scenes'])}"
        )

        return workflow