from agents.manager_agent import ManagerAgent


def main():

    topic = input("Topic: ").strip()

    if not topic:
        print("❌ Topic cannot be empty.")
        return

    manager = ManagerAgent()

    result = manager.run(topic)

    print("\n========== SEO ==========\n")
    print(result["seo"])

    print("\n========== SCRIPT ==========\n")
    print(result["script"])


if __name__ == "__main__":
    main()