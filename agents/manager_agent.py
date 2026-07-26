from workflow.workflow_engine import WorkflowEngine


class ManagerAgent:

    def __init__(self):

        self.workflow = WorkflowEngine()

    def run(self, topic):

        return self.workflow.run(topic)