import json

from workflow.workflow_engine import WorkflowEngine


def main():

    print("=" * 60)
    print("YouTube AI Studio")
    print("Workflow Engine Test")
    print("=" * 60)

    engine = WorkflowEngine()

    result = engine.run("AI Agents in 2026")

    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()