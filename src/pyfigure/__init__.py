from pathlib import Path
from tomlkit import load, parse, dump
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

    @dataclass
    class Config:
        pass

    defaults = {}
    config = {}

    def add_to_config(self, key, value, comment):
        self.config[key] = value
        if comment: self.config[key].comment(comment)

    def save_to_file(self):
        with open(self.config_file, 'w+') as file:
            dump(self.config, file)

    def load_from_file(self):
        with open(self.config_file, 'r') as file:
            self.config = load(file)
        i=0
        for key, value in self.defaults.items():
            if key not in self.config:
                i+=1
                self.add_to_config(key, value.default, value.description)
        if i: self.save_to_file()

    def reload_config(self):
        # default values
        self.defaults = self.Config.__annotations__
        self.config = parse("")
        for key, value in self.defaults.items():
            self.add_to_config(key, value.default, value.description)

        # config values
        if not self.config_file.exists():
            self.save_to_file()
        else:
            self.load_from_file()

        self.config = dict(self.config)
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


    def __init__(self, filename: str = f'{Path(argv[0]).stem}.toml'):
        if not hasattr(self, 'config_file'): self.config_file = Path(filename)
        self.reload_config()