import json

from agents.seo_agent import SEOAgent


def main():

    topic = "AI Agents in 2026"

    print("=" * 60)
    print("YouTube AI Studio")
    print("SEO Generator Test")
    print("=" * 60)

    seo = SEOAgent()

    result = seo.generate(topic)

    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()