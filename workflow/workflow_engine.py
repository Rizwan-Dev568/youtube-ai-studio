from agents.research_agent import ResearchAgent
from agents.seo_agent import SEOAgent
from agents.script_writer import ScriptWriter

from app.output_manager import OutputManager


class WorkflowEngine:

    def __init__(self):

        self.research = ResearchAgent()
        self.seo = SEOAgent()
        self.script = ScriptWriter()

    def run(self, topic):

        print("\n[1/3] Researching Topic...")
        research = self.research.research(topic)

        print("\n[2/3] Generating SEO...")
        seo = self.seo.generate(research)

        print("\n[3/3] Writing Script...")
        script = self.script.write_script(
            research,
            seo
        )

        result = {
            "topic": topic,
            "research": research,
            "seo": seo,
            "script": script,
        }

        OutputManager.save(
            topic,
            result
        )

        return result