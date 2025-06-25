import dataclasses
from typing import Literal, Optional, Any, Union, Tuple, List, Dict, Set

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
class TestModelWithListUnion(Validator):
    id: int
    name: str
    recommendations: List[Union[str, int]]


@dataclasses.dataclass(frozen=True)
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


@dataclasses.dataclass
class TestModelWithCustoms(Validator):
    list_items: List[TestInfo]
    set_items: Set[TestInfo]


def test_dataclass_validator__list_of_customs():
    model = TestModelWithCustoms(
        list_items=[TestInfo(id=1, name="Item1"), TestInfo(id=2, name="Item2")],
        set_items={TestInfo(id=1, name="Item1"), TestInfo(id=2, name="Item2")},
    )
    assert len(model.list_items) == 2
    for item in model.list_items:
        assert isinstance(item, TestInfo)
        assert isinstance(item.id, int)
        assert isinstance(item.name, str)

    try:
        model_invalid_list = TestModelWithCustoms(
            list_items=[TestInfo(id=1, name="Item1"), "InvalidItem"],
            set_items={TestInfo(id=1, name="Item1"), TestInfo(id=2, name="Item2")},
        )
    except TypeError as e:
        assert str(e) == (
            "Validation failed for TestModelWithCustoms: \n"
            "list_items: \n Expected: <class 'test_dataclass.TestInfo'> \n Received: <class 'str'>\n"
        )


def test_dataclass_validator__dict():
    model = TestModelWithDict(example={"test": 1})
    assert type(model.example) == dict
    assert type(model.example["test"]) == int

    try:
        model_invalid_dict = TestModelWithDict(example={"test": "string"})
    except TypeError as e:
        assert str(e) == (
            "Validation failed for TestModelWithDict: \n"
            "example: \n Expected: <class 'int'> \n Received: <class 'str'>\n"
        )


def test_dataclass_validator__tuple():
    model = TestModelWithTuple(example=("test", 1))
    assert type(model.example) == tuple
    assert type(model.example[0]) == str
    assert type(model.example[1]) == int

    try:
        model_invalid_tuple = TestModelWithTuple(example=("test", 2.5))
    except TypeError as e:
        assert str(e) == (
            "Validation failed for TestModelWithTuple: \n"
            "example: \n Expected: <class 'int'> \n Received: <class 'float'>\n"
        )

    try:
        model_invalid_tuple = TestModelWithTuple(example=("test", "string"))
    except TypeError as e:
        assert str(e) == (
            "Validation failed for TestModelWithTuple: \n"
            "example: \n Expected: <class 'int'> \n Received: <class 'str'>\n"
        )


def test_dataclass_validator__union():
    model_with_str = TestModelWithUnion(example="test")
    assert model_with_str.example == "test"
    assert type(model_with_str.example) == str

    model_with_int = TestModelWithUnion(example=1)
    assert model_with_int.example == 1
    assert type(model_with_int.example) == int

    try:
        model_violating_union = TestModelWithUnion(example=2.5)
    except TypeError as e:
        assert str(e) == (
            "Validation failed for TestModelWithUnion: \n"
            "example: \n Expected: (<class 'str'>, <class 'int'>) \n Received: <class 'float'>\n"
        )


def test_dataclass_validator__optional():
    model = TestModelWithOptional(id=2, name="Example", description="test1")

    model_without_description = TestModelWithOptional(id=2, name="Example")
    assert model_without_description.description is None


def test_dataclass_validator__any():
    types_to_test = [int, str, float, bool, type(None), dict, list, TestInfo]
    values_to_test = [
        1,
        "test",
        3.14,
        True,
        None,
        {"key": "value"},
        [1, 2, 3],
        TestInfo(id=1, name="Info"),
    ]
    for _type, value in zip(types_to_test, values_to_test):
        model = TestModelAny(id=value)
        assert model.id == value
        assert isinstance(model.id, _type)


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
    assert isinstance(model.info, TestInfo)

    try:
        model_with_wrong_custom_type = TestModelWithCustomType(
            info=TestModel(id=1, name="Example", description="test1")
        )
    except TypeError as e:
        assert str(e) == (
            "Validation failed for TestModelWithCustomType: \n"
            "info: \n Expected: <class 'test_dataclass.TestInfo'> \n Received: <class 'test_dataclass.TestModel'>\n"
        )


def test_dataclass_validator__list():
    model = TestModelWithList(id=1, name="Example", recommendations=["test1", "test2"])
    assert isinstance(model.recommendations, list)

    try:
        TestModelWithList(id=1, name="Example", recommendations=["test1", 2])
    except TypeError as e:
        assert str(e) == (
            "Validation failed for TestModelWithList: \n"
            "recommendations: \n Expected: <class 'str'> \n Received: <class 'int'>\n"
        )


def test_dataclass_validator__list_union():
    model = TestModelWithListUnion(id=1, name="Example", recommendations=["test1", 2])
    assert isinstance(model.recommendations, list)

    try:
        TestModelWithListUnion(id=1, name="Example", recommendations=["test1", 2.5])
    except TypeError as e:
        assert str(e) == (
            "Validation failed for TestModelWithListUnion: \n"
            "recommendations: \n Expected: (<class 'str'>, <class 'int'>) \n Received: <class 'float'>\n"
        )
