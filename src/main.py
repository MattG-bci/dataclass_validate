import dataclasses
from validate.dataclass import Validator



@dataclasses.dataclass
class BaseModel(Validator):
    id: int
    name: str
    description: str



if __name__== "__main__":
    model = BaseModel(id=1, name="Example", description="This is an example.")
    print(type(model))
