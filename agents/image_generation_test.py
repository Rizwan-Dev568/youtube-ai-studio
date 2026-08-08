"""
Image Generation Agent Test

Tests image generation agent structure
without making a real Gemini image request.
"""

from agents.image_generation_agent import (
    ImageGenerationAgent
)


def main():

    agent = ImageGenerationAgent()

    assert agent.service is not None

    assert agent.service.generator is not None

    assert agent.service.assets is not None

    print(
        "ImageGenerationAgent structure: OK"
    )


if __name__ == "__main__":

    main()