"""
Deep JSON Validator

Validates nested JSON structures
returned by AI.
"""


class DeepValidator:

    @classmethod
    def validate(
        cls,
        data,
        schema,
        path=""
    ):

        if not isinstance(schema, dict):

            return

        if not isinstance(data, dict):

            raise Exception(
                f"{path or 'root'} must be an object."
            )

        for key, expected in schema.items():

            if key not in data:

                raise Exception(
                    f"Missing key: {path + key}"
                )

            cls._validate_value(
                data[key],
                expected,
                path + key
            )

    @classmethod
    def _validate_value(
        cls,
        value,
        expected,
        path
    ):

        # Primitive types
        if isinstance(expected, type):

            if not isinstance(value, expected):

                raise Exception(
                    f"{path} should be "
                    f"{expected.__name__}, "
                    f"got {type(value).__name__}"
                )

            return

        # Nested object
        if isinstance(expected, dict):

            cls.validate(
                value,
                expected,
                path + "."
            )

            return

        # List
        if isinstance(expected, list):

            if not isinstance(value, list):

                raise Exception(
                    f"{path} should be list."
                )

            # Empty schema means accept any list
            if not expected:

                return

            item_schema = expected[0]

            for index, item in enumerate(value):

                cls._validate_value(
                    item,
                    item_schema,
                    f"{path}[{index}]"
                )

            return

        raise Exception(
            f"Unsupported schema at {path}"
        )