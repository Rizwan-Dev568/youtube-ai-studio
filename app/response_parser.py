"""
Response Parser
"""

from app.json_repair import JsonRepair


class ResponseParser:

    @staticmethod
    def parse(text):

        data = JsonRepair.loads(text)

        print("\n======================")
        print("PARSED DATA")
        print("======================")
        print(type(data))
        print(data.keys())
        print("======================\n")

        return data