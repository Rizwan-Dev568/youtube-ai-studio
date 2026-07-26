import os
import json
import hashlib


class CacheManager:

    def __init__(self):

        self.cache_folder = "cache"

        os.makedirs(
            self.cache_folder,
            exist_ok=True
        )

    def _filename(self, prompt):

        name = hashlib.md5(
            prompt.encode()
        ).hexdigest()

        return os.path.join(
            self.cache_folder,
            name + ".json"
        )

    def load(self, prompt):

        file = self._filename(prompt)

        if os.path.exists(file):

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        return None

    def save(self, prompt, response):

        file = self._filename(prompt)

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                response,
                f,
                ensure_ascii=False,
                indent=4
            )