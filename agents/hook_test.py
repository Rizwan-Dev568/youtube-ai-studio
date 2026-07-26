import json

from agents.hook_agent import HookAgent


def main():

    print("=" * 60)
    print("YouTube AI Studio")
    print("Hook Generator Test")
    print("=" * 60)

    topic = "AI Agents in 2026"

    agent = HookAgent()

    result = agent.generate(topic)

    print(
        json.dumps(
            result,
            indent=4
        )
    )


if __name__ == "__main__":
    main()