from agents.voice_prompt_agent import VoicePromptAgent


def main():

    script = {
        "title": "How to Build a No-Code AI Agent",
        "hook": "Imagine building an AI employee in just a few minutes.",
        "intro": (
            "In this video we'll build a complete AI agent "
            "without writing code."
        ),
        "sections": [
            "Introduction",
            "Step by step tutorial",
            "Final tips"
        ],
        "cta": (
            "Subscribe for more AI tutorials."
        ),
        "estimated_duration": "8 minutes"
    }

    agent = VoicePromptAgent()

    result = agent.generate(
        script
    )

    print("\n========== RESULT ==========\n")
    print(result)


if __name__ == "__main__":
    main()