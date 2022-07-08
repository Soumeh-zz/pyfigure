from pyfigure import Configurable, Option
from typing import Literal, List

class ExampleClass(Configurable):
    pass

    #config_file = 'other_file.toml'

    class Config:
        any_option = Option('any', "Any value works here")
        string_option: str = Option('default', "Any string works here")
        integer_option: int = Option(24, "Any integer here")
        float_option: float = Option(15.55, "Any float")
        bool_option: bool = Option(True, "Any boolean")
        list_option: list = Option(['e', 'a', 'o'], "A list of things")
        int_list_option: List[int] = Option([1, 2, 3], 'A list of integers')
        choice_option: Literal['spam', 'eggs'] = Option('spam', 'Either "spam" or "eggs"')
        class sub_config:
            sub_option: str = Option('this value in a sub value')
            class sub_sub_config:
                sub_sub_option: str = Option('this value is a sub value of a sub value')

    #def __init__(self):
    #    Configurable.__init__(self)

ec = ExampleClass()
print(ec.config)

def test_once():
    ec = ExampleClass()
    assert 'any_option' in ec.config

def test_edit():
    ec = ExampleClass()
    with open(ec.config_file, 'r') as file:
        lines = file.readlines()
    lines[0] = "any_option = 3 # Any value works here\n"
    with open(ec.config_file, "w") as file:
        file.writelines(lines)
    assert ec.config.any_option == 3