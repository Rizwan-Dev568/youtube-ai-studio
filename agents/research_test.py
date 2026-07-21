from agents.research_agent import ResearchAgent

agent = ResearchAgent()

result = agent.research("Artificial Intelligence")

print("\n========== TOPIC ==========")
print(result["topic"])

print("\n========== REPORT ==========")
for key, value in result["report"].items():
    print(f"{key}: {value}")

print("\n========== TOP VIDEOS ==========")

for video in result["videos"][:5]:
    print("-" * 50)
    print("Title :", video["title"])
    print("Views :", video["views"])
    print("Likes :", video["likes"])
    print("Comments :", video["comments"])
    print("Score :", video["score"])