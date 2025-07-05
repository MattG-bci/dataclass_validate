import dataclasses
from validate.dataclass import Validator
from typing import Literal, Optional, Any, Union, Tuple, List, Dict, Set
from enum import Enum


@dataclasses.dataclass
class Model(Validator):
    id: int
    name: str
    description: Literal["test1", "test2", "test3"]


@dataclasses.dataclass
class ModelWithList(Validator):
    id: int
    name: str
    recommendations: List[str]


@dataclasses.dataclass
class ModelWithListUnion(Validator):
    id: int
    name: str
    recommendations: List[Union[str, int]]


@dataclasses.dataclass(frozen=True)
class Info:
    id: int
    name: str


@dataclasses.dataclass
class ModelWithCustomType(Validator):
    info: Info


@dataclasses.dataclass
class ModelAny(Validator):
    id: Any


@dataclasses.dataclass
class ModelWithOptional(Validator):
    id: int
    name: str
    description: Optional[str] = None


@dataclasses.dataclass
class ModelWithUnion(Validator):
    example: Union[str, int]


@dataclasses.dataclass
class ModelWithTuple(Validator):
    example: Tuple[str, int]


@dataclasses.dataclass
class ModelWithDict(Validator):
    example: Dict[str, int]


@dataclasses.dataclass
class ModelWithCustoms(Validator):
    list_items: List[Info]
    set_items: Set[Info]


@dataclasses.dataclass
class ModelChild(Model):
    additional_info: str


@dataclasses.dataclass
class ModelWithInheritance(Validator):
    data: Model


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


@dataclasses.dataclass
class ModelEnum(Validator):
    status: Status
