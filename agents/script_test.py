import json

from agents.script_writer import ScriptWriter


def main():

    topic = "AI Agents in 2026"

    print("=" * 60)
    print("YouTube AI Studio")
    print("Script Writer Test")
    print("=" * 60)

    writer = ScriptWriter()

    result = writer.write_script(topic)

    print(
        json.dumps(
            result,
            indent=4,
            ensure_ascii=False
        )
    )


if __name__ == "__main__":
    main()