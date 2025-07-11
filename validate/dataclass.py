import dataclasses
from abc import ABC, abstractmethod
import typing
from typing import Any, Union
from enum import EnumMeta

from validate.utils import (
    generate_failed_validation_message,
    pair_values_with_types,
)

SIMPLE_TYPES: list[type] = [
    int,
    str,
    float,
    bool,
    list,
    dict,
    set,
    tuple,
]


class BaseValidator(ABC):
    def __init__(self):
        self._SUPPORTED_TYPES = {
            typing._LiteralGenericAlias: self._handle_literal_types,
            typing._UnionGenericAlias: self._handle_generic_union_type,
            EnumMeta: self._handle_simple_types,
        } | dict.fromkeys(SIMPLE_TYPES, self._handle_simple_types)

        self._ITERABLE_TYPES = {
            typing.List: self._validate_list,
            typing.Set: self._validate_list,
            typing._GenericAlias: self._validate_tuple,
        }

    @staticmethod
    @abstractmethod
    def _handle_generic_union_type(
        field: dataclasses.Field, value: Any
    ) -> Union[str, None]:
        pass

    @staticmethod
    @abstractmethod
    def _handle_literal_types(field: dataclasses.Field, value: Any) -> Union[str, None]:
        pass

    @staticmethod
    @abstractmethod
    def _handle_simple_types(field: dataclasses.Field, value: Any) -> Union[str, None]:
        pass

    @abstractmethod
    def _validate_tuple(self, field: dataclasses.Field, value: Any) -> Union[str, None]:
        pass

    @abstractmethod
    def _validate_list(self, field: dataclasses.Field, value: Any) -> Union[str, None]:
        pass

    @abstractmethod
    def _validate(self) -> None:
        pass

    @abstractmethod
    def __post_init__(self) -> None:
        pass


class Validator(BaseValidator):
    def __post_init__(self) -> None:
        super().__init__()
        self._validate()

    def _validate(self) -> None:
        failed_validations = []
        for field in dataclasses.fields(self):
            value = getattr(self, field.name)

            iterable_type_validator = self._ITERABLE_TYPES.get(
                field.type, self._ITERABLE_TYPES.get(field.type.__class__)
            )
            if iterable_type_validator:
                failed_validation = iterable_type_validator(field, value)
                if failed_validation:
                    failed_validations.append(failed_validation)

            else:
                failed_validation = self._validate_single_object(field, value)
                if failed_validation:
                    failed_validations.append(failed_validation)

        if failed_validations:
            raise TypeError(
                f"Validation failed for {self.__class__.__name__}: \n"
                + "".join(failed_validations)
            )

    def _validate_single_object(
        self, field: dataclasses.Field, value: Any
    ) -> Union[str, None]:
        field_type = field.type
        if field_type == Any:
            return

        if hasattr(field_type, "__annotations__"):
            type_handler = self._handle_simple_types
        else:
            type_handler = self._SUPPORTED_TYPES.get(
                field_type, self._SUPPORTED_TYPES.get(field_type.__class__)
            )

        if not type_handler:
            raise Exception(f"Type not supported: {field.type}")

        res = type_handler(field, value)
        return res

    def _validate_list(self, field: dataclasses.Field, value: Any) -> Union[str, None]:
        for item in value:
            sub_field = dataclasses.field()
            sub_field.type = (
                field.type.__args__[0]
                if hasattr(field.type, "__args__")
                else field.type
            )
            sub_field.name = field.name
            res = self._validate_single_object(sub_field, item)
            if res:
                return res
        return

    def _validate_tuple(self, field: dataclasses.Field, value: Any) -> Union[str, None]:
        if isinstance(value, typing.Dict):
            value = [(k, v) for k, v in value.items()]

        elif isinstance(value, typing.Tuple):
            value = [value]

        target_types = field.type.__args__
        pairs_to_check = pair_values_with_types(value, target_types)
        for item, target_type in pairs_to_check:
            sub_field = dataclasses.field()
            sub_field.type = target_type
            sub_field.name = field.name
            res = self._validate_single_object(sub_field, item)
            if res:
                return res
        return

    @staticmethod
    def _handle_generic_union_type(
        field: dataclasses.Field, value: Any
    ) -> Union[str, None]:
        for type_in_union in field.type.__args__:
            if isinstance(value, type_in_union):
                return
        return generate_failed_validation_message(
            field.name, field.type.__args__, type(value)
        )

    @staticmethod
    def _handle_simple_types(field: dataclasses.Field, value: Any) -> Union[str, None]:
        if not isinstance(value, field.type):
            return generate_failed_validation_message(
                field.name, field.type, type(value)
            )
        return

    @staticmethod
    def _handle_literal_types(field: dataclasses.Field, value: Any) -> Union[str, None]:
        if value not in field.type.__args__:
            return generate_failed_validation_message(
                field.name, field.type.__args__, value
            )
        return
