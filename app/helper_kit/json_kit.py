from flask import json


class JsonKit:

    @staticmethod
    def convert_to_json(json_string: str):
        result = None

        if json_string is not None:
            try:
                result = json.loads(json_string)

            except Exception as e:
                return None

        return result

    @staticmethod
    def convert_to_json_string(value):
        return json.dumps(value)
