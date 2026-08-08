"""
Professional Memory Manager

Stores workflow memory, topic history,
scores, and workflow resume state.
"""

import json
from pathlib import Path
from datetime import datetime


class MemoryManager:

    MEMORY_FILE = (
        Path(__file__).parent
        / "memory_store.json"
    )

    MAX_HISTORY = 100

    def __init__(self):

        self.MEMORY_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.MEMORY_FILE.exists():

            self._save({})

    # -----------------------
    # Internal
    # -----------------------

    def _load(self):

        try:

            with open(
                self.MEMORY_FILE,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            # Corrupted / missing JSON
            self._save({})
            return {}

    def _save(
        self,
        data
    ):

        with open(
            self.MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    # -----------------------
    # Simple Key / Value
    # -----------------------

    def set(
        self,
        key,
        value
    ):

        data = self._load()

        data[key] = {
            "value": value,
            "updated": datetime.utcnow().isoformat()
        }

        self._save(data)

    def get(
        self,
        key,
        default=None
    ):

        data = self._load()

        if key not in data:

            return default

        return data[key].get(
            "value",
            default
        )

    def exists(
        self,
        key
    ):

        return key in self._load()

    def delete(
        self,
        key
    ):

        data = self._load()

        if key in data:

            del data[key]

            self._save(data)

    # -----------------------
    # Topic History
    # -----------------------

    def add_topic(
        self,
        topic
    ):

        topic = topic.strip()

        data = self._load()

        history = data.get(
            "topic_history",
            {
                "value": [],
                "updated": ""
            }
        )

        topics = history["value"]

        if topic not in topics:

            topics.append(topic)

        topics = topics[-self.MAX_HISTORY:]

        data["topic_history"] = {
            "value": topics,
            "updated": datetime.utcnow().isoformat()
        }

        self._save(data)

    def topic_exists(
        self,
        topic
    ):

        return topic.strip() in self.get(
            "topic_history",
            []
        )

    def recent_topics(
        self,
        limit=10
    ):

        return self.get(
            "topic_history",
            []
        )[-limit:]

    # -----------------------
    # Workflow Resume
    # -----------------------

    def save_step(
        self,
        step_name,
        result
    ):

        self.set(
            step_name,
            result
        )

    def load_step(
        self,
        step_name
    ):

        return self.get(
            step_name
        )

    def clear_step(
        self,
        step_name
    ):

        self.delete(
            step_name
        )

    # -----------------------
    # Best Workflow
    # -----------------------

    def save_best_workflow(
        self,
        workflow,
        score
    ):

        best = self.get(
            "best_workflow"
        )

        if (
            best is None
            or score > best["score"]
        ):

            self.set(
                "best_workflow",
                {
                    "score": score,
                    "workflow": workflow
                }
            )

    # -----------------------
    # Utility
    # -----------------------

    def clear(self):

        self._save({})

    def keys(self):

        return list(
            self._load().keys()
        )

    def all(self):

        return self._load()