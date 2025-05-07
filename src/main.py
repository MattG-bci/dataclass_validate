import dataclasses
from validate.dataclass import Validator


@dataclasses.dataclass
class BaseModel(Validator):
    id: int
    name: str
    description: str


