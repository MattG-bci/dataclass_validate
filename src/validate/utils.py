from typing import Any


def generate_failed_validation_message(field_name: str, expected_value: Any, received_value: Any) -> str:
    return f"{field_name}: \n Expected: {expected_value} \n Received: {received_value}\n"


def pair_elements(values, types) -> list:
    if len(types) == 1:
        return [(val, types[0]) for val in values]
    else:
        return [pair for value in values for pair in list(zip(value, types))]
