"""
Schema Validator

Validates AI output against schemas.
"""


class SchemaValidator:

    @staticmethod
    def validate(data, schema):

        if not isinstance(data, dict):

            return (
                False,
                "Response is not a dictionary."
            )

        # Check required keys
        for key, expected_type in schema.items():

            if key not in data:

                return (
                    False,
                    f"Missing key: {key}"
                )

            if not isinstance(
                data[key],
                expected_type
            ):

                return (
                    False,
                    f"{key} should be "
                    f"{expected_type.__name__}, "
                    f"got {type(data[key]).__name__}"
                )

        return (
            True,
            "Valid"
        )