import ctypes
from enum import Enum

from ...core.configuration.conditions import ListCondition
from .base_ctype import CTypeTuple, BaseCStructure, ConfigParams, Endianness


class NumType(Enum):
    Byte = CTypeTuple("byte", "c", ctypes.c_char)  # byte (8 bit)
    Short = CTypeTuple("short", "h", ctypes.c_int16)  # short (16 bit)
    Int = CTypeTuple("int", "i", ctypes.c_int32)  # int (32 bit)
    Long = CTypeTuple("long", "q", ctypes.c_int64)  # long long (64 bit)


class BaseNumType(BaseCStructure):
    __config__ = {
        ConfigParams.type: ListCondition(NumType, default=NumType.Byte),
        ConfigParams.endianness: ListCondition(Endianness, default=Endianness.Little),
    }


Byte = BaseNumType < BaseNumType.config.Type.Byte
Short = BaseNumType < BaseNumType.config.Type.Short
Int = BaseNumType < BaseNumType.config.Type.Int
Long = BaseNumType < BaseNumType.config.Type.Long
