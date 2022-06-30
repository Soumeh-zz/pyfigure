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
from typing import Literal, List

class ExampleClass(Configurable):

    #config_file = 'other_file.toml'

    class Config:
        string_option: str = Option("default", "Any string works here.")
        integer_option: int = Option(24, "Any integer here.")
        float_option: float = Option(15.55, "Any float.")
        bool_option: bool = Option(True, "Any boolean.")
        list_option: list = Option(['e', 'a', 'o'], "A list of things.")
        int_list_option: List[int] = Option([1, 2, 3], 'A list of integers.')
        choice_option: Literal['spam', 'eggs'] = Option('spam', "A list of random things")

    def __init__(self):
        Configurable.__init__(self)
        print(self.config)


ExampleClass()
```

This class, when initialized, will print:

```py
{
	'string_option': 'default',
	'integer_option': 24,
	'float_option': 15.55,
	'bool_option': True,
	'list_option': ['e', 'a', 'o'],
	'int_list_option': [1, 2, 3],
	'choice_option': 'spam'
}
```

And create a new file:

`file.toml`
```toml
[config]
string_option = "default" # Any string works here.
integer_option = 24 # Any integer here.
float_option = 15.55 # Any float.
bool_option = true # Any boolean.
list_option = ["e", "a", "o"] # A list of things.
int_list_option = [1, 2, 3] # A list of integers.
choice_option = "spam" # A list of random things

```

## To-Do

- ~~Rework the type checking system to utilize the `typing` library (Somehow).~~ Done, the project now depends on [typeguard](https://github.com/agronholm/typeguard).
- Support nested dictionaries.