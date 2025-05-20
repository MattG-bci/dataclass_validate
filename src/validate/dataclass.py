import dataclasses
from abc import ABC, abstractmethod
import typing
from typing import Any, Optional, Tuple
import collections.abc

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
            typing.Any: self._handle_any_type,
            typing._UnionGenericAlias: self._handle_generic_union_type,
        } | dict.fromkeys(SIMPLE_TYPES, self._handle_simple_types)

        self._ITERABLE_TYPES = {
            typing.List: self._validate_list,
            typing.Set: self._validate_list,
            typing._GenericAlias: self._validate_tuple,
        }


    @staticmethod
    @abstractmethod
    def _handle_generic_union_type(field: dataclasses.Field, value: Any) -> Optional[str]:
        pass

    @staticmethod
    def _handle_any_type(field: dataclasses.Field, value: Any) -> None:
        return

    @staticmethod
    @abstractmethod
    def _handle_literal_types(field: dataclasses.Field, value: Any) -> Optional[str]:
        pass

    @staticmethod
    @abstractmethod
    def _handle_simple_types(field: dataclasses.Field, value: Any) -> Optional[str]:
        pass

    @abstractmethod
    def _validate_tuple(self, field: dataclasses.Field, value: Any) -> Optional[str]:
        pass

    @abstractmethod
    def _validate_list(self, field: dataclasses.Field, value: Any) -> Optional[str]:
        pass

    @abstractmethod
    def _validate(self) -> None:
        pass

    @abstractmethod
    def __post_init__(self):
        pass


class Validator(BaseValidator):
    def __post_init__(self):
        super().__init__()
        self._validate()

    def _validate(self):
        failed_validations = []
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)

            iterable_type_validator = self._ITERABLE_TYPES.get(field.type, self._ITERABLE_TYPES.get(field.type.__class__))
            if iterable_type_validator:
                failed_validation = iterable_type_validator(field, value)
                if failed_validation:
                    failed_validations.append(failed_validation)

            else:
                failed_validation = self._validate_single_object(field, value)
                if failed_validation:
                    failed_validations.append(failed_validation)

        if failed_validations:
            raise TypeError(f"Validation failed for {self.__class__.__name__}: \n" + "".join(failed_validations))

    def _validate_single_object(self, field: dataclasses.Field, value: Any) -> Optional[str]:
        field_type = field.type
        if hasattr(field_type, "__dict__") and "__annotations__" in field_type.__dict__:
            type_handler = self._handle_simple_types
        else:
            type_handler = self._SUPPORTED_TYPES.get(
                field_type,
                self._SUPPORTED_TYPES.get(field_type.__class__)
            )

        if not type_handler:
            raise Exception(f"Type not supported: {field.type}")

        res = type_handler(field, value)
        return res

    def _validate_list(self, field: dataclasses.Field, value: Any) -> Optional[str]:
        for item in value:
            sub_field = dataclasses.field()
            sub_field.type = field.type.__args__[0] if hasattr(field.type, "__args__") else field.type
            sub_field.name = field.name
            res = self._validate_single_object(sub_field, item)
            if res:
                return res
        return

    def _validate_tuple(self, field: dataclasses.Field, value: Any) -> Optional[str]:
        for item, target_type in zip(value, field.type.__args__):
            sub_field = dataclasses.field()
            sub_field.type = target_type
            sub_field.name = field.name
            res = self._validate_single_object(sub_field, item)
            if res:
                return res
        return

    @staticmethod
    def _handle_generic_union_type(field: dataclasses.Field, value: Any) -> Optional[str]:
        for type_in_union in field.type.__args__:
            if isinstance(value, type_in_union):
                return
        return generate_failed_validation_message(
            field.name,
            field.type.__args__,
            type(value)
        )

    @staticmethod
    def _handle_simple_types(field: dataclasses.Field, value: Any) -> Optional[str]:
        if not isinstance(value, field.type):
            return generate_failed_validation_message(
                field.name,
                field.type,
                type(value)
            )
        return

    @staticmethod
    def _handle_literal_types(field: dataclasses.Field, value: Any) -> Optional[str]:
        if value not in field.type.__args__:
            return generate_failed_validation_message(
                    field.name,
                    field.type.__args__,
                    value
                )
        return
