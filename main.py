"""
YouTube AI Studio

Main Entry Point
"""

from agents.manager_agent import ManagerAgent


def main():

    print("=" * 60)
    print("      YouTube AI Studio V7")
    print("=" * 60)

    topic = input(
        "\nEnter YouTube Topic:\n> "
    ).strip()

    if not topic:

        print("\nTopic cannot be empty.")

        return

    manager = ManagerAgent()

    workflow = manager.run(topic)

    print("\n")
    print("=" * 60)
    print("PROJECT COMPLETED")
    print("=" * 60)

    print(
        f"Final Title : {workflow['director']['final_title']}"
    )

    print(
        f"Score : {workflow['director']['overall_score']}"
    )

    print(
        f"Approved : {workflow['director']['approved']}"
    )


if __name__ == "__main__":

    main()