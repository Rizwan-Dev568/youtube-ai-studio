"""
Reviewer Agent Test
"""

from agents.reviewer_agent import ReviewerAgent


def main():

    reviewer = ReviewerAgent()

    research = {
        "topic": "Artificial Intelligence"
    }

    seo = {
        "titles": [
            "Best AI Video"
        ]
    }

    title_rank = {
        "winner": "Best AI Video"
    }

    hooks = {
        "hooks": [
            "This will change everything..."
        ]
    }

    thumbnail = {
        "thumbnail_title": "AI"
    }

    script = {
        "title": "AI",
        "hook": "Hook",
        "intro": "Intro",
        "sections": [
            "One",
            "Two",
            "Three"
        ],
        "cta": "Subscribe",
        "estimated_duration": "10 minutes"
    }

    result = reviewer.review(
        research,
        seo,
        title_rank,
        hooks,
        thumbnail,
        script
    )

    print(result)


if __name__ == "__main__":
    main()