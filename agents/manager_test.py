from agents.manager_agent import ManagerAgent


def main():

    topic = input("Topic: ").strip()

    if not topic:
        print("Topic cannot be empty.")
        return

    manager = ManagerAgent()

    result = manager.run(topic)

    print("\n========== RESEARCH ==========\n")
    print(result["research"])

    print("\n========== SEO ==========\n")
    print(result["seo"])

    print("\n========== HOOKS ==========\n")
    print(result["hooks"])

    print("\n========== THUMBNAIL ==========\n")
    print(result["thumbnail"])

    print("\n========== SCRIPT ==========\n")
    print(result["script"])


if __name__ == "__main__":
    main()