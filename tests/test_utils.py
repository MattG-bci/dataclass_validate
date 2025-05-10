from validate.utils import generate_failed_validation_message


def test_generate_failed_validation_message():
    assert generate_failed_validation_message("field", "expected", "received") == (
        "field: \n Expected: expected \n Received: received\n"
    )


