from src.validate.utils import generate_failed_validation_message
from src.validate.utils import pair_values_with_types


def test_generate_failed_validation_message():
    assert generate_failed_validation_message("field", "expected", "received") == (
        "field: \n Expected: expected \n Received: received\n"
    )


def test_pair_values_with_types():
    assert pair_values_with_types([1, 2, 3], [int]) == [(1, int), (2, int), (3, int)]
    assert pair_values_with_types([(1, 2), (3, 4)], [int, int]) == [
        (1, int),
        (2, int),
        (3, int),
        (4, int),
    ]
    assert pair_values_with_types(["a", "b"], [str]) == [("a", str), ("b", str)]
