"""
The base class for all structures.
"""
from stoat.base_structure import BaseStructure
from stoat.type_factory import TypeFactory
from stoat.array import Array


class Structure(BaseStructure):
    @classmethod
    def array(cls, size):
        return TypeFactory(Array, cls, size)

    @classmethod
    def param(cls, parameter):
        return TypeFactory(cls, parameter)
