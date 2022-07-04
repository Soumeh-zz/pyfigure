from pathlib import Path
from typing import Callable, Any
from dataclasses import dataclass
from sys import argv
from inspect import isclass

from tomlkit import document, load, dump, table
from typeguard import check_type

@dataclass
class Option:
    default: Any
    description: str = ''
    parse: Callable = lambda x: x

class Configurable:

    @dataclass
    class Config:
        pass

    def __init__(self, file: Path = Path(argv[0]).with_suffix('').with_suffix('.toml')):
        self.config = table(True)
        if not hasattr(self, 'config_file'): self.config_file = file
        self.config_file = Path(self.config_file)

        self.reload_config()

    def reload_config(self):
        # set default values
        self._defaults = {}
        self._generate_config(self.Config, self._defaults)

        # get config values
        if self.config_file.exists():
            self._load_config()
            self._append_default(self._defaults, self.config)
            self._save_config()
            self._parse_config(self._defaults, self.config)
        else:
            self._append_default(self._defaults, self.config)
            self._parse_config(self._defaults, self.config)
            self._save_config()
        
        del self._defaults

    def _save_config(self):
        with open(self.config_file, 'w+') as file:
            dump(self.config, file)

    def _load_config(self):
        with open(self.config_file, 'r') as file:
            for key, value in load(file).items():
                self.config[key] = value

    def _append_default(self, nest, destination):
        for key, value in nest.items():

            if isinstance(value, dict):
                if not key in destination: destination[key] = table()
                self._append_default(nest[key], destination[key])
                continue

            if key in destination: continue
            destination[key] = value.default
            if value.description:
                destination.value.item(key).comment(value.description)

    def _parse_config(self, nest, destination):
        for key, value in destination.items():

            if isinstance(value, dict):
                if key not in nest: continue
                self._parse_config(nest[key], destination[key])
                continue

            if key not in nest:
                continue
            data = nest[key]

            try:
                check_type(key, value, data.default_type)
            except TypeError as error:
                value = data.default
                self._parse_error(key, error)

            try:
                value = data.parse(value)
            except Exception as error:
                value = data.default
                self._parse_error(key, error)

            destination[key] = value
            setattr(destination, key, value)
            if hasattr(value, 'description'):
                destination.value.item(key).comment(value.description)

    def _generate_config(self, nest, destination):
        if '__annotations__' in nest.__dict__:
            for key, default_type in nest.__dict__['__annotations__'].items():
                destination[key] = nest.__dict__[key]
                destination[key].default_type = default_type
        for nest in nest.__dict__.values():
            if not isclass(nest): continue
            destination[nest.__name__] = {}
            self._generate_config(nest, destination[nest.__name__])

    def _parse_error(self, option, message):
        print(f"Error while trying to load option '{option}': {message}")