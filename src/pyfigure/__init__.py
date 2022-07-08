from pathlib import Path
from typing import Callable, Any
from dataclasses import dataclass, fields
from sys import argv
from inspect import isclass
from copy import copy

from tomlkit import document, load, dump, table
from typeguard import check_type
from superdict import SuperDict

class SuperDict(SuperDict):
    pass

@dataclass
class Option:
    default: Any
    description: str = ''
    parse: Callable = lambda x: x

class Configurable:

    @dataclass
    class Config:
        pass

    def __init__(self):
        # set up config file
        if not hasattr(self, 'config_file'): self.config_file = Path(argv[0]).with_suffix('').with_suffix('.toml')
        self.config_file = Path(self.config_file)

        # reload once to generate
        self.reload_config()

    def reload_config(self):
        # set default values
        self._defaults = {}
        self.config = table()
        self._generate_config(self.Config, self._defaults)

        # if a config file was already generated
        if self.config_file.exists():
            # load the config, update it if needed and parse it
            self._load_config()
            temp = copy(self.config)
            self._append_default(self._defaults, self.config)
            # only save if values were missing
            if dict(self.config) != dict(temp): self._save_config()
            self._parse_config(self._defaults, self.config)
        else:
            # create a new config, parse it and save it
            self._append_default(self._defaults, self.config)
            self._parse_config(self._defaults, self.config)
            self._save_config()
        self.config = SuperDict(self.config)
        
        del self._defaults

    def _save_config(self):
        with open(self.config_file, 'w+') as file:
            dump(self.config, file)

    def _load_config(self):
        with open(self.config_file, 'r') as file:
            for key, value in load(file).items():
                self.config[key] = value

    def _append_default(self, nest, destination):
        # go over the default values
        for key, value in nest.items():

            # if dict, loop over it
            if isinstance(value, dict):
                if not key in destination: destination[key] = table()
                self._append_default(nest[key], destination[key])
                continue

            # if the value is already in the config, ignore it
            if key in destination: continue
            destination[key] = value.default

            # add comments
            if value.description:
                destination.value.item(key).comment(value.description)

    def _parse_config(self, nest, destination):
        # go over every value in the config
        for key, value in destination.items():

            # if the value isn't in the default values, ignore it
            if key not in nest: continue

            # if dict, loop over it
            if isinstance(value, dict):
                self._parse_config(nest[key], destination[key])
                continue

            data = nest[key]

            # check the value's type
            try:
                check_type(key, value, data.default_type)
            # if incorrect, thrown an error, and use the default value
            except TypeError as check_error:
                destination[key] = data.default
                self._parse_error(key, check_error)

            # parse the value
            try:
                destination[key] = data.parse(value)
            # if unable, thrown an error, and use the default value
            except Exception as parse_error:
                destination[key] = data.default
                self._parse_error(key, parse_error)

    def _generate_config(self, nest, destination):

        # get config values and default values
        values = {_:value for _, value in nest.__dict__.items() if isinstance(value, Option)}

        # stop if no values
        if not values: return

        defaults = nest.__dict__['__annotations__']

        # remove non-values
        for key, _ in values.copy().items():
            if key.startswith('__'):
                del values[key]

        # iter over values
        for key, value in values.items():

            # if Option object, process it
            if isinstance(value, Option):
                destination[key] = value
                if key in defaults:
                    destination[key].default_type = defaults[key]
                else:
                    destination[key].default_type = Any
            # else, loop over it
            else:
                destination[value.__name__] = {}
                self._generate_config(value, destination[value.__name__])

    def _parse_error(self, option, message):
        print(f"Error while trying to load option '{option}': {message}")
