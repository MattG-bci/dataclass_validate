import dataclasses
from src.validate.dataclass import Validator


def test_dataclass_validator():

    @dataclasses.dataclass
    class TestModel(Validator):
        id: int
        name: str
        description: str

    model = TestModel(id=1, name="Example", description="This is an example.")
    assert isinstance(model, Validator)
    assert type(model.id) == int
    assert type(model.name) == str
    assert type(model.description) == str
