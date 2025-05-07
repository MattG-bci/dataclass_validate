import dataclasses


@dataclasses.dataclass
class Validator:
    def __post_init__(self):
        failed_validation = []
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                failed_validation.append(f"{field.name}: \n Expected: {field.type} \n Received: {type(value)}\n")

        if failed_validation:
            raise TypeError(f"Validation failed for {self.__class__.__name__}: \n" + "".join(failed_validation))
