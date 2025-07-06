# dataclass_validate

## Overview

This repository provides a Python package for validating dataclasses using a custom class for validation, `Validator`.
It allows you to validate types for your dataclass fields and ensures that the data conforms to these types
right after the dataclass objects are instantiated.

The usage is made to be straightforward. All it needs to be done is to inherit from the `Validator`
and... that's it! The validation will be done automatically.

## Example


```python 
from dataclasses import dataclass
from validate.dataclass import Validator

@dataclass
class Person(Validator):
    name: str
    age: int

person = Person(name="John", age=30)  # This will pass validation
person_invalid = Person(name="John", age="30")  # This will raise a TypeError
```

## Installation

```
pip install dataclass-validate 
```

## Further Information

Although the package is simple to use, there are a few things to keep in mind:
- The validation is done AFTER the instantiation of the dataclass object.
- If the validation fails, a `TypeError` will be raised. It follows strong typing by design.
- The package provides a support for simple types like `int`, `str`, `float`, and `bool`
as well as the types coming from the `typing` module like `List`, `Dict`, and `Optional`. On top of that,
`Validator` validates custom types as well!
- The validation follows the rules of the type hierarchy, meaning that if a field is of type `List[bool]`
and user provides a heterogeneous list such as `[True, True, 3]`, this will raise an error.
- As of now, the package does not support modern Python syntax for union types such as `int | str`.

## Further Work
- Add support for modern syntax for union types like `int | str`. 
- Expand towards more complex types like Iterators, Generators, and more.