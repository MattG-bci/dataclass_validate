import dataclasses
from typing import Literal, Optional, Any, Union, Tuple, List, Dict

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
    recommendations: List[str]


@dataclasses.dataclass
class TestInfo:
    id: int
    name: str

@dataclasses.dataclass
class TestModelWithCustomType(Validator):
    info: TestInfo


@dataclasses.dataclass
class TestModelAny(Validator):
    id: Any


@dataclasses.dataclass
class TestModelWithOptional(Validator):
    id: int
    name: str
    description: Optional[str] = None


@dataclasses.dataclass
class TestModelWithUnion(Validator):
    example: Union[str, int]


@dataclasses.dataclass
class TestModelWithTuple(Validator):
    example: Tuple[str, int]


@dataclasses.dataclass
class TestModelWithDict(Validator):
    example: Dict[str, int]



def test_dataclass_validator__dict():
    model = TestModelWithDict(example={"test": 1})
    assert isinstance(model, Validator)
    assert model.example == {"test": 1}
    assert type(model.example) == dict
    assert len(model.example) == 1
    assert type(model.example["test"]) == int


def test_dataclass_validator__tuple():
    model = TestModelWithTuple(example=("test", 1))
    assert isinstance(model, Validator)
    assert model.example == ("test", 1)
    assert type(model.example) == tuple
    assert len(model.example) == 2
    assert type(model.example[0]) == str
    assert type(model.example[1]) == int


def test_dataclass_validator__union():
    model = TestModelWithUnion(example="test")
    assert isinstance(model, Validator)
    assert model.example == "test"
    assert type(model.example) == str

    model_with_int = TestModelWithUnion(example=1)
    assert isinstance(model_with_int, Validator)
    assert model_with_int.example == 1
    assert type(model_with_int.example) == int


def test_dataclass_validator__optional():
    model = TestModelWithOptional(id=2, name="Example", description="test1")
    assert isinstance(model, Validator)

    model_without_description = TestModelWithOptional(id=2, name="Example")
    assert isinstance(model_without_description, Validator)


def test_dataclass_validator__any():
    model = TestModelAny(id=2)
    assert isinstance(model, Validator)
    assert model.id == 2
    assert type(model.id) == int


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


def test_dataclass_validator__custom_type():
    model = TestModelWithCustomType(info=TestInfo(id=2, name="Info"))
    assert isinstance(model, Validator)
    assert isinstance(model.info, TestInfo)


def test_dataclass_validator__list():
    model = TestModelWithList(id=1, name="Example", recommendations=["test1", "test2"])
    assert isinstance(model, Validator)
    assert isinstance(model.recommendations, list)
