import dataclasses
import abc
import typing

from src.utils import generate_failed_validation_message

class Validator(abc.ABC):
    def __post_init__(self):
        failed_validations = []
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)

            if field.type.__class__ == typing._LiteralGenericAlias:
                # Handle Literal types
                if value not in field.type.__args__:
                    failed_validations.append(
                        generate_failed_validation_message(
                            field.name,
                            field.type.__args__,
                            value
                        )
                    )
            else:
                if not isinstance(value, field.type):
                    failed_validations.append(
                        generate_failed_validation_message(
                            field.name,
                            field.type,
                            type(value)
                        )
                    )

        if failed_validations:
            raise TypeError(f"Validation failed for {self.__class__.__name__}: \n" + "".join(failed_validations))
