from conftest import *
from validate.dataclass import Validator


def test_dataclass_validator__enum():
    model = ModelEnum(status=Status.ACTIVE)
    assert isinstance(model.status, Status)
    assert model.status == Status.ACTIVE

    try:
        ModelEnum(status=Status.INACTIVE)
    except TypeError as e:
        assert str(e) == (
            "Validation failed for ModelEnum: \n"
            "status: \n Expected: <enum 'Status'> \n Received: <class 'str'>\n"
        )


def test_dataclass_validator__inheritance():
    model = ModelWithInheritance(
        ModelChild(id=1, name="Example", description="test1", additional_info="extra")
    )
    assert isinstance(model.data, ModelChild)
    assert isinstance(model.data, Model)

    assert ModelWithInheritance(data=Model(id=1, name="Example", description="test1"))


def test_dataclass_validator__list_of_customs():
    model = ModelWithCustoms(
        list_items=[Info(id=1, name="Item1"), Info(id=2, name="Item2")],
        set_items={Info(id=1, name="Item1"), Info(id=2, name="Item2")},
    )
    assert len(model.list_items) == 2
    for item in model.list_items:
        assert isinstance(item, Info)
        assert isinstance(item.id, int)
        assert isinstance(item.name, str)

    try:
        ModelWithCustoms(
            list_items=[Info(id=1, name="Item1"), "InvalidItem"],
            set_items={Info(id=1, name="Item1"), Info(id=2, name="Item2")},
        )
    except TypeError as e:
        assert str(e) == (
            "Validation failed for ModelWithCustoms: \n"
            "list_items: \n Expected: <class 'conftest.Info'> \n Received: <class 'str'>\n"
        )


def test_dataclass_validator__dict():
    model = ModelWithDict(example={"test": 1})
    assert isinstance(model.example, dict)
    assert isinstance(model.example["test"], int)

    try:
        ModelWithDict(example={"test": "string"})
    except TypeError as e:
        assert str(e) == (
            "Validation failed for ModelWithDict: \n"
            "example: \n Expected: <class 'int'> \n Received: <class 'str'>\n"
        )


def test_dataclass_validator__tuple():
    model = ModelWithTuple(example=("test", 1))
    assert isinstance(model.example, tuple)
    assert isinstance(model.example[0], str)
    assert isinstance(model.example[1], int)

    try:
        ModelWithTuple(example=("test", 2.5))
    except TypeError as e:
        assert str(e) == (
            "Validation failed for ModelWithTuple: \n"
            "example: \n Expected: <class 'int'> \n Received: <class 'float'>\n"
        )

    try:
        ModelWithTuple(example=("test", "string"))
    except TypeError as e:
        assert str(e) == (
            "Validation failed for ModelWithTuple: \n"
            "example: \n Expected: <class 'int'> \n Received: <class 'str'>\n"
        )


def test_dataclass_validator__union():
    model_with_str = ModelWithUnion(example="test")
    assert model_with_str.example == "test"
    assert isinstance(model_with_str.example, str)

    model_with_int = ModelWithUnion(example=1)
    assert model_with_int.example == 1
    assert isinstance(model_with_int.example, int)

    try:
        ModelWithUnion(example=2.5)
    except TypeError as e:
        assert str(e) == (
            "Validation failed for ModelWithUnion: \n"
            "example: \n Expected: (<class 'str'>, <class 'int'>) \n Received: <class 'float'>\n"
        )


def test_dataclass_validator__optional():
    model = ModelWithOptional(id=2, name="Example", description="test1")
    assert isinstance(model.id, int)
    assert isinstance(model.name, str)
    assert isinstance(model.description, str) or model.description is None

    model_without_description = ModelWithOptional(id=2, name="Example")
    assert model_without_description.description is None


def test_dataclass_validator__any():
    types_to_test = [int, str, float, bool, type(None), dict, list, Info]
    values_to_test = [
        1,
        "test",
        3.14,
        True,
        None,
        {"key": "value"},
        [1, 2, 3],
        Info(id=1, name="Info"),
    ]
    for _type, value in zip(types_to_test, values_to_test):
        model = ModelAny(id=value)
        assert model.id == value
        assert isinstance(model.id, _type)


def test_dataclass_validator():
    model = Model(id=1, name="Example", description="test1")
    assert isinstance(model, Validator)


def test_dataclass_validator__invalid_literal():
    try:
        Model(id=1, name="Example", description="test4")
    except TypeError as e:
        assert str(e) == (
            "Validation failed for Model: \n"
            "description: \n Expected: ('test1', 'test2', 'test3') \n Received: test4\n"
        )


def test_dataclass_validator__custom_type():
    model = ModelWithCustomType(info=Info(id=2, name="Info"))
    assert isinstance(model.info, Info)

    try:
        ModelWithCustomType(info=Model(id=1, name="Example", description="test1"))
    except TypeError as e:
        assert str(e) == (
            "Validation failed for ModelWithCustomType: \n"
            "info: \n Expected: <class 'conftest.Info'> \n Received: <class 'conftest.Model'>\n"
        )


def test_dataclass_validator__list():
    model = ModelWithList(id=1, name="Example", recommendations=["test1", "test2"])
    assert isinstance(model.recommendations, list)

    try:
        ModelWithList(id=1, name="Example", recommendations=["test1", 2])
    except TypeError as e:
        assert str(e) == (
            "Validation failed for ModelWithList: \n"
            "recommendations: \n Expected: <class 'str'> \n Received: <class 'int'>\n"
        )


def test_dataclass_validator__list_union():
    model = ModelWithListUnion(id=1, name="Example", recommendations=["test1", 2])
    assert isinstance(model.recommendations, list)

    try:
        ModelWithListUnion(id=1, name="Example", recommendations=["test1", 2.5])
    except TypeError as e:
        assert str(e) == (
            "Validation failed for ModelWithListUnion: \n"
            "recommendations: \n Expected: (<class 'str'>, <class 'int'>) \n Received: <class 'float'>\n"
        )
