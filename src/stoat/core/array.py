"""
The Array class handles the containment of other structure classes into array
stypes.
"""
from .meta_structure import MetaStructure
from .config.conditions import IntCondition, TypeCondition
from .base_structure import BaseStructure


class ConstantSize:
    def __init__(self, value):
        self.value = value


class Array(BaseStructure):
    _config = {
        "size": IntCondition(exact=True, more=True, default=0),
        "cls": TypeCondition(type=MetaStructure),
    }

    def __init__(self, _parent=None):
        super().__init__(_parent=_parent)
        self.data = [self.cls() for _ in range(self.size)]

    @property
    def size(self):
        return self._config.get("size")

    @property
    def cls(self):
        return self._config.get("cls")

    def calcsize(self):
        size = super().calcsize()
        for value in self.data:
            size += value.calcsize()
        return size

    def pack_into(self, buffer, offset):
        offset = super().pack_into(buffer, offset)
        for value in self.data:
            offset = value.pack_into(buffer, offset)
        return offset

    @classmethod
    def unpack_from(cls, buffer, offset, _parent=None):
        result, offset = super().unpack_from(buffer, offset, _parent=_parent)
        result.data = [None] * result.size
        for i in range(result.size):
            result.data[i], offset = result.cls.unpack_from(buffer, offset, _parent=result)
        return result, offset

    def _set(self, value):
        if self.size == len(value):
            for index, item in enumerate(value):
                self_assignment = self.data[index]._set(item)
                if self_assignment:
                    self.data[index] = self_assignment
        else:
            raise TypeError('value list must be of the same size ('
                            f'expected {self.size} got {len(value)})')

    def __getitem__(self, item):
        return self.data[item]._get()

    def __setitem__(self, key, value):
        self_assignment = self.data[key]._set(value)
        if self_assignment:
            self.data[key] = self_assignment

    def __eq__(self, other):
        try:
            if self.size == len(other):
                return all((v == o for v, o in zip(self.data, other)))
            else:
                return False
        except TypeError:
            return super().__eq__(other)

    def __len__(self):
        return self.size

    @classmethod
    def array(cls, size):
        # raise Exception('you are probably doing something wrong')
        return Array < {
            "size": cls._config.get("size"),
            "cls": cls._config.get("cls")[size],
        }

    @classmethod
    def iter(cls):
        raise TypeError('cannot unpack non-iterable Structure class {name}'
                        .format(name=cls.__name__))

    @classmethod
    def _updated_config(cls, config):
        # If this is a defined array type then reconfiguring will change the internal type
        if cls._config.get("cls"):
            new_cls = cls._config.get("cls").reconfigure(config)
            new_config = cls._config.update({"cls": new_cls})
            return new_config
        # Otherwise this a new definition of an array type in which case we create the array
        else:
            assert cls._config.validate(config)
            return cls._config.update(config)

    # @classmethod
    # def reconfigure(cls, config):
    #     new_cls = cls._config.get("cls").reconfigure(config)
    #     new_config = cls._config.update({"cls": new_cls})
    #     key = (cls._uuid, new_config)
    #     if not cls._get_class(key):
    #         new_type = cls.copy()
    #         new_type._config = new_config
    #         return cls._get_class(key, new_type)
    #     else:
    #         cls._get_class(key)
