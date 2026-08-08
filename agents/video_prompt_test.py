from agents.video_prompt_agent import VideoPromptAgent


def main():

    image_prompts = {
        "images": [
            {
                "scene": 1,
                "title": "Opening",
                "image_prompt": (
                    "A young AI developer working on multiple "
                    "monitors in a modern office, cinematic "
                    "lighting, ultra realistic, 16:9"
                ),
                "negative_prompt": "",
                "style": "Cinematic Realistic",
                "aspect_ratio": "16:9"
            }
        ]
    }

    agent = VideoPromptAgent()

    result = agent.generate(
        image_prompts
    )

    print("\n========== RESULT ==========\n")
    print(result)


if __name__ == "__main__":
    main()