import dataclasses
from validate.dataclass import Validator



@dataclasses.dataclass
class BaseModel(Validator):
    id: int
    name: str
    description: str



if __name__== "__main__":
    model = BaseModel(id="1", name=None, description=123123)
    print(type(model))
