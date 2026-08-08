from agents.character_profile_agent import CharacterProfileAgent


def main():

    script = {
        "title": "The Lost Robot",
        "hook": "A lonely robot begins an unforgettable journey.",
        "intro": "A young engineer discovers an abandoned robot.",
        "sections": [
            "The discovery",
            "The adventure",
            "The ending"
        ],
        "cta": "Subscribe for more AI stories.",
        "estimated_duration": "8 minutes"
    }

    scene_plan = {
        "scenes": [
            {
                "scene": 1,
                "title": "Discovery",
                "narration": "The engineer finds the robot in an old warehouse.",
                "visual": "Young engineer looking at a dusty robot.",
                "camera": "Wide Shot",
                "emotion": "Curious",
                "lighting": "Soft daylight",
                "duration": "8 seconds",
                "transition": "Fade"
            }
        ]
    }

    agent = CharacterProfileAgent()

    result = agent.generate(
        script,
        scene_plan
    )

    print("\n========== RESULT ==========\n")
    print(result)


if __name__ == "__main__":
    main()