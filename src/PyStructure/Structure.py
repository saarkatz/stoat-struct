"""
The base class for all structures.
"""
from PyStructure.BaseStructure import BaseStructure
from PyStructure.TypeFactory import TypeFactory
from PyStructure.Array import Array


class Structure(BaseStructure):
    @classmethod
    def array(cls, size):
        return TypeFactory(Array, cls, size)

    @classmethod
    def param(cls, parameter):
        return TypeFactory(cls, parameter)
