"""
This file defines the meta class for the structure class.
Here the functionality over the structure class is implemented.
"""
from abc import ABCMeta
from collections import OrderedDict
from stoat.base_type_factory import BaseTypeFactory


class MetaStructure(ABCMeta):
    def __new__(mcs, name, bases, dictionary):
        result = super().__new__(mcs, name, bases, dictionary)
        result._structure = OrderedDict()

        # Collect all the classes of MetaStructure and instances of
        # BaseTypeFactory into the structure dictionary.
        for attribute, value in dictionary.items():
            if isinstance(value, (MetaStructure, BaseTypeFactory)):
                result._structure[attribute] = value

        return result

    def __getitem__(cls, size):
        return cls.array(size)

    def __add__(cls, parameter):
        return cls.param(parameter)

    def __iter__(cls):
        raise cls.iter()
