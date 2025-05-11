import dataclasses
from abc import ABC, abstractmethod
import typing
from typing import Any, Union

from src.validate._types import SIMPLE_TYPES
from src.validate.utils import generate_failed_validation_message


# str, int, float, bool, list, dict, set, tuple
# list[str], dict[str, int], set[int], tuple[float, str]
# Literal, Optional, Union, Any
# Custom data types (dataclasses, enums, etc.)

class BaseValidator(ABC):
    def __init__(self):
        self._SUPPORTED_TYPES = {
            typing._LiteralGenericAlias: self._handle_literal_types,
        } | dict.fromkeys(SIMPLE_TYPES, self._handle_simple_types)

    @staticmethod
    @abstractmethod
    def _handle_literal_types(field: dataclasses.Field, value: Any) -> Union[str, None]:
        pass

    @abstractmethod
    def _validate(self) -> None:
        pass

    @abstractmethod
    def __post_init__(self):
        pass


class Validator(BaseValidator):
    def __init__(self):
        super().__init__()

    def __post_init__(self):
        self._validate()


    def _validate(self) -> None:
        failed_validations = []
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)
            field_type = field.type

            if field_type in SIMPLE_TYPES:
                type_handler = self._SUPPORTED_TYPES.get(field_type)
            elif field_type.__class__ in self._SUPPORTED_TYPES:
                type_handler = self._SUPPORTED_TYPES.get(field_type.__class__)
            # Check if the field type is a custom type
            elif "__annotations__" in field_type.__dict__:
                type_handler = self._handle_simple_types
            else:
                type_handler = None

            if not type_handler:
                raise Exception(f"Type not supported: {field.type}")

            res = type_handler(field, value)
            if res:
                failed_validations.append(res)

        if failed_validations:
            raise TypeError(f"Validation failed for {self.__class__.__name__}: \n" + "".join(failed_validations))


    @staticmethod
    def _handle_simple_types(field: dataclasses.Field, value: Any) -> Union[str, None]:
        if not isinstance(value, field.type):
            return generate_failed_validation_message(
                field.name,
                field.type,
                type(value)
            )
        return


    @staticmethod
    def _handle_literal_types(field: dataclasses.Field, value: Any) -> Union[str, None]:
        if value not in field.type.__args__:
            return generate_failed_validation_message(
                    field.name,
                    field.type.__args__,
                    value
                )
        return
