from agents.image_prompt_agent import ImagePromptAgent


def main():

    scene_plan = {
        "scenes": [
            {
                "scene": 1,
                "title": "Opening",
                "narration": "A young AI developer starts building a YouTube AI Studio.",
                "visual": "Developer working on multiple monitors.",
                "camera": "Wide cinematic shot",
                "emotion": "Focused",
                "lighting": "Blue ambient",
                "duration": "8 seconds",
                "transition": "Fade"
            }
        ]
    }

    agent = ImagePromptAgent()

    result = agent.generate(
        scene_plan
    )

    print("\n========== RESULT ==========\n")
    print(result)


if __name__ == "__main__":
    main()