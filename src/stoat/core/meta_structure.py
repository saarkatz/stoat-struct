"""
This file defines the meta class for the structure class.
Here the functionality over the structure class is implemented.
"""
from abc import ABCMeta
from collections import OrderedDict
from uuid import uuid4
from .config import Config
from stoat.auxiliary.config_builder import ConfigBuilder

# Dictionary that holds all the generated classes
_structure_classes_dict = {}


class MetaStructure(ABCMeta):
    # A class generated using new (new is called when using the class key word)
    # will always be its own class.
    def __new__(mcs, name, bases, dictionary, uuid=None):
        dictionary = OrderedDict(dictionary)
        config = dictionary.pop("_config", {})
        result = super().__new__(mcs, name, bases, dictionary)
        result._structure = OrderedDict()
        result._config = Config(getattr(result, "_config", {})).merge(config)
        result._uuid = uuid if uuid else uuid4()

        # Collect all the classes of MetaStructure into the structure dictionary.
        for attribute, value in dictionary.items():
            if isinstance(value, MetaStructure):
                result._structure[attribute] = value

        _structure_classes_dict[(result._uuid, result._config)] = result
        return result

    # Square bracket operator -> Create array
    def __getitem__(cls, size):
        return cls.array(size)

    # Classes generated through configuration change will be looked for in the
    # dictionary
    def __lt__(cls, config):
        return cls.reconfigure(config)

    # Usage might be used to unpack a structure
    def __iter__(cls):
        return cls.iter()

    def array(cls, size):
        raise NotImplementedError(
            "Array method not implemented for type {}".format(cls.__name__))

    def iter(cls):
        raise NotImplementedError(
            "Iter method not implemented for type {}".format(cls.__name__))

    def copy(cls):
        # Get the base structure class of cls
        key = cls._get_base_key()
        base_strcuture = MetaStructure._get_class(key, cls)

        new_cls = MetaStructure.__new__(
            MetaStructure,
            base_strcuture.__name__,
            (base_strcuture,),  # Inherit the base structure class
            base_strcuture.__dict__,
            base_strcuture._uuid
        )
        return new_cls

    def _updated_config(cls, config):
        assert cls._config.validate(config)
        return cls._config.update(config)

    def _configure(cls, config):
        key = (cls._uuid, config)
        if not MetaStructure._get_class(key):
            new_type = cls.copy()
            new_type._config = new_type._config(config)
            return cls._get_class(key, new_type)
        else:
            return _structure_classes_dict[key]

    def reconfigure(cls, config):
        # Support for ConfigBuilder auxiliary without bake command
        if isinstance(config, ConfigBuilder):
            config = config.bake()

        return cls._configure(cls._updated_config(config))

    def _get_key(cls):
        return cls._uuid, cls._config

    def _get_base_key(cls):
        return cls._uuid, cls._config.default()

    def __eq__(self, other):
        return (
            isinstance(other, MetaStructure)
            and self._get_key() == other._get_key()
        )

    @classmethod
    def _get_class(mcs, key, default=None):
        if default and key not in _structure_classes_dict:
            _structure_classes_dict[key] = default
        return _structure_classes_dict.get(key, None)
