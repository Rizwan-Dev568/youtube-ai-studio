from agents.research_agent import ResearchAgent

agent = ResearchAgent()

videos = agent.research("Artificial Intelligence")

for video in videos[:5]:
    print(video)