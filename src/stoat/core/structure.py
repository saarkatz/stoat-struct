"""
The base class for all structures.
"""
from stoat.core.base_structure import BaseStructure
from stoat.core.array import Array


class Structure(BaseStructure):
    @classmethod
    def array(cls, size):
        return Array < {
            "size": size,
            "cls": cls,
        }


def reconfigure(cls, config):
    return cls < config
