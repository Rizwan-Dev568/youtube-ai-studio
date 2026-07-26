from app.gemini_client import GeminiClient


def main():

    print("=" * 60)
    print("YouTube AI Studio")
    print("Gemini Test")
    print("=" * 60)

    ai = GeminiClient()

    result = ai.ask(
        "Write one sentence about Artificial Intelligence."
    )

    print(result)


if __name__ == "__main__":
    main()