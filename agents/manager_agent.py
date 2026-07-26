from agents.research_agent import ResearchAgent
from agents.seo_agent import SEOAgent
from agents.hook_agent import HookAgent
from agents.thumbnail_agent import ThumbnailAgent
from agents.script_writer import ScriptWriter


class ManagerAgent:

    def __init__(self):

        self.research = ResearchAgent()
        self.seo = SEOAgent()
        self.hook = HookAgent()
        self.thumbnail = ThumbnailAgent()
        self.script = ScriptWriter()

    def run(self, topic):

        print("\n[1/5] Researching Topic...")
        research = self.research.research(topic)

        print("\n[2/5] Generating SEO...")
        seo = self.seo.generate(research)

        print("\n[3/5] Generating Hooks...")
        hooks = self.hook.generate(
            research,
            seo
        )

        print("\n[4/5] Generating Thumbnail...")
        thumbnail = self.thumbnail.generate(
            research,
            seo
        )

        print("\n[5/5] Writing Script...")
        script = self.script.write_script(
            research,
            seo
        )

        return {
            "research": research,
            "seo": seo,
            "hooks": hooks,
            "thumbnail": thumbnail,
            "script": script
        }