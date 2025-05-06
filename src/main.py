import dataclasses


@dataclasses.dataclass
class DataclassValidator:
    def __init__(self, cls):
        self.cls = cls

    def __post_init__(self):
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                raise TypeError(f"Field {field.name} must be of type {field.type.__name__}")



@dataclasses.dataclass
class BaseModel(DataclassValidator):
    id: int
    name: str
    description: str



if __name__== "__main__":
    model = BaseModel(id=1, name="Example", description="This is an example.")
    print(type(model))
