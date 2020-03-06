"""
The base class for all structures.
"""
from stoat.BaseStructure import BaseStructure
from stoat.TypeFactory import TypeFactory
from stoat.Array import Array


class Structure(BaseStructure):
    @classmethod
    def array(cls, size):
        return TypeFactory(Array, cls, size)

    @classmethod
    def param(cls, parameter):
        return TypeFactory(cls, parameter)
