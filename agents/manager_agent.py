from agents.research_agent import ResearchAgent
from agents.seo_agent import SEOAgent
from agents.title_ranker_agent import TitleRankerAgent
from agents.hook_agent import HookAgent
from agents.thumbnail_agent import ThumbnailAgent
from agents.script_writer import ScriptWriter


class ManagerAgent:

    def __init__(self):

        self.research = ResearchAgent()
        self.seo = SEOAgent()
        self.title_ranker = TitleRankerAgent()
        self.hook = HookAgent()
        self.thumbnail = ThumbnailAgent()
        self.script = ScriptWriter()

    def run(self, topic):

        print("\n[1/6] Researching Topic...")
        research = self.research.research(topic)

        print("\n[2/6] Generating SEO...")
        seo = self.seo.generate(research)

        print("\n[3/6] Ranking Titles...")
        title_rank = self.title_ranker.generate(
            seo["titles"]
        )

        print("\n[4/6] Generating Hooks...")
        hooks = self.hook.generate(
            research,
            seo
        )

        print("\n[5/6] Generating Thumbnail...")
        thumbnail = self.thumbnail.generate(
            research,
            seo
        )

        print("\n[6/6] Writing Script...")
        script = self.script.write_script(
            research,
            seo
        )

        return {
            "research": research,
            "seo": seo,
            "title_rank": title_rank,
            "hooks": hooks,
            "thumbnail": thumbnail,
            "script": script,
        }