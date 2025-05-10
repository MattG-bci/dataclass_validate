import dataclasses
from typing import Literal

from src.validate.dataclass import Validator


@dataclasses.dataclass
class TestModel(Validator):
    id: int
    name: str
    description: Literal["test1", "test2", "test3"]


def test_dataclass_validator():
    model = TestModel(id=1, name="Example", description="test1")
    assert isinstance(model, Validator)


def test_dataclass_validator__invalid_literal():
    try:
        TestModel(id=1, name="Example", description="test4")
    except TypeError as e:
        assert str(e) == (
            "Validation failed for TestModel: \n"
            "description: \n Expected: ('test1', 'test2', 'test3') \n Received: test4\n"
        )
