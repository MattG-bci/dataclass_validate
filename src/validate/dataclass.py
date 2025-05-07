import dataclasses


@dataclasses.dataclass
class Validator:
    def __post_init__(self):
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                raise TypeError(f"Field {field.name} must be of type {field.type.__name__}")

