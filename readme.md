# pyfigure

Generate configuration files for classes.

## Installation

`pip install pyfigure`

## Usage

To generate a configuration file for a class, you must extend the class with `Configurable`, from the `pyfigure` module.

Then, to add options to the configuration, create a new `Config` class, and add variables of the `Option` class.

```py
option_name: Option(
    default,
    type,
    parse,
    description,
)
```

### Where the arguments are as follows:

|argument|description|default value|
|-|-|-|
`default`|The default value of the option|`n/a`
`type`|The python type the option is|`str`
`parse`|A function that parses the given value, returns a new value or throws an exception|`lambda x: x`
`description`|A comment to explain what the option is for|`n/a`

`file.py`
```py
from pyfigure import Configurable, Option

class SomeClass(Configurable):

    class Config:
        string_option: Option("default", str, description="Any string works here.")
        integer_option: Option(24, int, description="Any integer here.")
        float_option: Option(15.55, float, description="Any float.")
    
    def __init__(self):
        super().__init__()
        print(self.config)
        # {'string_option': 'default', 'integer_option': 24, 'float_option': 15.55}

SomeClass()
```

This class, when initialized, will create a new file named:

`file.toml`
```toml
string_option = "default" # Any string works here.
integer_option = 24 # Any integer here.
float_option = 15.55 # Any float.
```

> Need to place the file at a different location?
Simply pass an argument in the `super().__init__()` function.

```py
def __init__(self):
    super().__init__('new/location/file.toml')
```

## To-Do

- Rework the type checking system to utilize the `typing` library. Somehow.