import ctypes
from enum import Enum

from ...core.configuration.conditions import ListCondition
from .base_ctype import CTypeTuple, BaseCStructure, ConfigParams, Endianness


class CharType(Enum):
    Char = CTypeTuple("char", "c", ctypes.c_char)  # char (8 bit)


class BaseCharType(BaseCStructure):
    __config__ = {
        ConfigParams.type: ListCondition(CharType, default=CharType.Char),
        ConfigParams.endianness: ListCondition(Endianness, default=Endianness.Little),
    }

    def getter(self):
        return chr(self.data.value[0])

    def setter(self, value):
        try:
            self.data.value = ord(value)
        except TypeError:
            super().setter(value)


Char = BaseCharType < BaseCharType.config.Type.Char

