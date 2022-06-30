from pathlib import Path
from typing import Callable, Any
from dataclasses import dataclass
from sys import argv

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
        for key, default_type in self.Config.__dict__['__annotations__'].items():
            self._defaults[key] = self.Config.__dict__[key]
            self._defaults[key].default_type = default_type

        # get config values
        if self.config_file.exists():
            self._load_config()
            self._add_to_config()
        else:
            self._add_to_config()
            self._save_config()

        # parse values
        for key, value in self.config.items():

            if key not in self._defaults:
                continue
            data = self._defaults[key]

            try:
                check_type(key, value, data.default_type)
            except TypeError as error:
                self._parse_error(key, error)

            try:
                value = data.parse(value)
            except Exception as error:
                self._parse_error(key, error)
                continue

            self.config[key] = value
            setattr(self.config, key, value)

        del self._defaults

    def _save_config(self):
        with open(self.config_file, 'w+') as file:
            doc = document()
            doc['config'] = self.config
            dump(doc, file)

    def _load_config(self):
        with open(self.config_file, 'r') as file:
            self.config = load(file)
        if 'config' in self.config: self.config = self.config['config']

    def _add_to_config(self):
        different = False
        for key, value in self._defaults.items():
            if key not in self.config:
                different = True
                self.config[key] = value.default
                if value.description:
                    self.config.value.item(key).comment(value.description)
        if different: self._save_config()

    def _parse_error(self, option, message):
        print(f"Error while trying to load option '{option}': {message}")
        self.config[option] = self._defaults[option].default