import dataclasses
from typing import Literal

import pytest

from src.validate.dataclass import Validator


@dataclasses.dataclass
class TestModel(Validator):
    id: int
    name: str
    description: Literal["test1", "test2", "test3"]


@dataclasses.dataclass
class TestModelWithList(Validator):
    id: int
    name: str
    recommendations: list[str]


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

@pytest.mark.skip(reason="Still implementing the support for parameterised lists")
def test_dataclass_validator__list():
    model = TestModelWithList(id=1, name="Example", recommendations=["test1", "test2"])
