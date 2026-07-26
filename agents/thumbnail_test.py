import json

from agents.thumbnail_agent import ThumbnailAgent


def main():

    print("=" * 60)
    print("YouTube AI Studio")
    print("Thumbnail Intelligence Test")
    print("=" * 60)

    topic = "AI Agents in 2026"

    agent = ThumbnailAgent()

    result = agent.generate(topic)

    print(
        json.dumps(
            result,
            indent=4
        )
    )


if __name__ == "__main__":
    main()