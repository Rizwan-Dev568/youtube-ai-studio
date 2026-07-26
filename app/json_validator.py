```python
import json


class JSONValidator:

    @staticmethod
    def validate(text):

        try:
            return json.loads(text)

        except Exception:
            return None 