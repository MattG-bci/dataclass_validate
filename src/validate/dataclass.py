import dataclasses
import abc
import typing


class Validator(abc.ABC):
    def __post_init__(self):
        failed_validations = []
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)

            if field.type.__class__ == typing._LiteralGenericAlias:
                # Handle Literal types
                if value not in field.type.__args__:
                    failed_validations.append(f"{field.name}: \n Expected: {field.type.__args__} \n Received: {value}\n")

            else:
                if not isinstance(value, field.type):
                    failed_validations.append(f"{field.name}: \n Expected: {field.type} \n Received: {type(value)}\n")

        if failed_validations:
            raise TypeError(f"Validation failed for {self.__class__.__name__}: \n" + "".join(failed_validations))
