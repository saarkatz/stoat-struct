"""
The base class for all structures.
"""
from stoat.core.base_structure import BaseStructure
from stoat.core.type_factory import TypeFactory
from stoat.core.array import Array


class Structure(BaseStructure):
    @classmethod
    def array(cls, size):
        return TypeFactory(Array, cls, size)

    @classmethod
    def param(cls, parameter):
        return TypeFactory(cls, parameter)
