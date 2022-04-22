from pathlib import Path
from tomlkit import document, load, dump, table
from typing import Callable, Any
from dataclasses import dataclass
from sys import argv

@dataclass
class Option:
    default: Any
    type: type = str
    parse: Callable = lambda x: x
    description: str = ''

class Configurable:

    defaults = {}
    def __init__(self, file: Path = Path(argv[0]).with_suffix('').with_suffix('.toml')):
        self.config = table()
        self.config_file = file
        self.reload_config()

    @dataclass
    class Config:
        pass

    def add_to_config(self, key, value, comment):
        self.config[key] = value
        if comment:
            self.config.value.item(key).comment(comment)

    def save_to_file(self):
        with open(self.config_file, 'w+') as file:
            doc = document()
            doc['config'] = self.config
            dump(doc, file)

    def load_from_file(self):
        with open(self.config_file, 'r') as file:
            self.config = load(file)
        if 'config' in self.config: self.config = self.config['config']

        different = False
        for key, value in self.defaults.items():
            if key not in self.config:
                different = True
                self.add_to_config(key, value.default, value.description)
        if different: self.save_to_file()

    def reload_config(self):
        # default values
        try:
            self.defaults = self.Config.__annotations__
        except AttributeError:
            self.config = {}
            return
        for key, value in self.defaults.items():
            self.add_to_config(key, value.default, value.description)

        # config values
        if not self.config_file.exists():
            self.save_to_file()
        else:
            self.load_from_file()

        # parse values
        for key, value in self.config.items():
            if key not in self.defaults:
                continue
            if not isinstance(value, self.defaults[key].type):
                self.parse_error(key, "Type needs to be " + self.defaults[key].type.__name__)
                continue
            try:
                value = self.defaults[key].parse(value)
            except Exception as error:
                self.parse_error(key, error)
                continue
            self.config[key] = value
        
        delattr(self, 'defaults')

    def parse_error(self, option, message):
        print(f"Error while trying to load option '{option}': {message}")
        self.config[option] = self.defaults[option].default