from agents.research_agent import ResearchAgent
from agents.seo_agent import SEOAgent
from agents.title_ranker_agent import TitleRankerAgent
from agents.hook_agent import HookAgent
from agents.thumbnail_agent import ThumbnailAgent
from agents.script_writer import ScriptWriter

from app.output_manager import OutputManager


class ManagerAgent:

    def __init__(self):

        self.research = ResearchAgent()
        self.seo = SEOAgent()
        self.title_ranker = TitleRankerAgent()
        self.hook = HookAgent()
        self.thumbnail = ThumbnailAgent()
        self.script = ScriptWriter()

    def run(self, topic):

        print("\n[1/7] Researching Topic...")

        research = self.research.research(topic)
        OutputManager.save(
            "research",
            research
        )

        print("\n[2/7] Generating SEO...")

        seo = self.seo.generate(research)
        OutputManager.save(
            "seo",
            seo
        )

        print("\n[3/7] Ranking Titles...")

        title_rank = self.title_ranker.generate(
            seo["titles"]
        )

        OutputManager.save(
            "title_rank",
            title_rank
        )

        print("\n[4/7] Generating Hooks...")

        hooks = self.hook.generate(
            research,
            seo
        )

        OutputManager.save(
            "hooks",
            hooks
        )

        print("\n[5/7] Generating Thumbnail...")

        thumbnail = self.thumbnail.generate(
            research,
            seo
        )

        OutputManager.save(
            "thumbnail",
            thumbnail
        )

        print("\n[6/7] Writing Script...")

        script = self.script.write_script(
            research,
            seo
        )

        OutputManager.save(
            "script",
            script
        )

        workflow = {
            "research": research,
            "seo": seo,
            "title_rank": title_rank,
            "hooks": hooks,
            "thumbnail": thumbnail,
            "script": script,
        }

        OutputManager.save(
            "workflow",
            workflow
        )

        print("\n[7/7] Workflow Complete.")

        return workflow