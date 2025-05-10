from typing import Any


def generate_failed_validation_message(field_name: str, expected_value: Any, received_value: Any) -> str:
    return f"{field_name}: \n Expected: {expected_value} \n Received: {received_value}\n"


