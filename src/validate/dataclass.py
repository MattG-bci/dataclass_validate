import dataclasses
import abc


class Validator(abc.ABC):
    def __post_init__(self):
        failed_validations = []
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, field.type):
                failed_validations.append(f"{field.name}: \n Expected: {field.type} \n Received: {type(value)}\n")

        if failed_validations:
            raise TypeError(f"Validation failed for {self.__class__.__name__}: \n" + "".join(failed_validations))
