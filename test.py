from dataclasses import dataclass
from pyfigure import Configurable, Option

class SomeClass(Configurable):

    class Config:
        string_option: Option("default", str, description="Any string works here.")
        integer_option: Option(24, int, description="Any integer here.")
        float_option: Option(15.55, float, description="Any float.")
        bool_option: Option(True, bool, description="Any boolean.")
    
    def __init__(self):
        super().__init__()
        print(self.config)
        # {'string_option': 'default', 'integer_option': 24, 'float_option': 15.55, 'bool_option': True}

SomeClass()