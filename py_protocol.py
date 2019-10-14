"""
This module defines the infrastructure for the simple definition of binary
protocols.
Requires python >= 3.6
"""
import ctypes
import struct
from functools import partial
from collections import OrderedDict


class MetaProtocol(type):
    """
    Meta class for the protocol class.
    This class provides the following properties to its instance classes:
     *  property(cls, *args, **kwargs) method
        Returns a property generated from the class using its internally
        defined get and set functions. This will be used for access to the
        attribute of instances of the class.
     *  Preparing any attribute in the instance class that is itself an
        instance class or an instance of one:
         *  Aggregate all such attribute to an ordered structure dictionary.
         *  Generate a property for each such attribute that will replace
            these attributes in their place.
     *  Implement the __getitem__ builtin for array generation using square
        brackets.  # TODO: Implement __getitem__
    """
    def property(cls, *args, **kwargs):
        return property(
            partial(cls._get, *args,
                    cls=cls, **kwargs) if '_get' in dir(cls) else None,
            partial(cls._set, *args,
                    cls=cls, **kwargs) if '_set' in dir(cls) else None,
            partial(cls._del, *args,
                    cls=cls, **kwargs) if '_del' in dir(cls) else None,
            doc=str(cls.__doc__)
        )

    def __new__(mcs, name, bases, dictionary):
        result = super().__new__(mcs, name, bases, dictionary)
        if '_structure' not in dir(result):
            result._structure = OrderedDict()
        elif '_structure' not in result.__dict__:
            result._structure = result._structure.copy()

        for attribute, value in dictionary.items():
            if isinstance(value, MetaProtocol):
                result._structure[attribute] = value
                setattr(result, attribute, value.property(attribute))
        return result

    def __getitem__(cls, item):
        return cls.array(item)


class Protocol(metaclass=MetaProtocol):
    """
    Base class for all protocols.
    This class provides the basic logic needed for the operation of a protocol:
     *  Initialization of the protocol data layer based on the structure
        dictionary.
    """
    def __init__(self, *args, **kwargs):
        """Initialize the data layer of the protocol"""
        self._data = OrderedDict()
        for field, protocol in self._structure.items():
            self._data[field] = protocol(*args, **kwargs)

    def calcsize(self, *args, **kwargs):
        """Calculate the size of the protocols current state"""
        size = 0
        for data_field in self._data.values():
            size += data_field.calcsize(*args, **kwargs)
        return size

    def pack(self, *args, **kwargs):
        """Return a binary string representation of the current state of the
        protocol"""
        size = self.calcsize()
        binstate = bytearray(size)
        self.pack_into(binstate, 0, *args, **kwargs)
        return bytes(binstate)

    def pack_into(self, buffer, offset, *args, **kwargs):
        """Fill the buffer with the data representation of the current state
        of the protocol"""
        for data_field in self._data.values():
            offset = data_field.pack_into(buffer, offset, *args, **kwargs)
        return offset

    @staticmethod
    def unpack(data, *args, **kwargs):
        """Instantiate the protocol from some binary data"""
        pass

    def get(self, **kwargs):
        """This method defines the way data should be received from a
        protocol object of this type"""
        return self

    def set(self, value, cls, **kwargs):
        """This method defines the way data should be set from a protocol
        object of this type. The updated protocol should always be returned
        to allow for protocols that are their own data"""
        if not isinstance(value, cls):
            raise ValueError('')  # TODO: make an appropriate exception class
        return value

    @staticmethod
    def _get(attribute, instance, cls, **kwargs):
        """This method defines how to access this protocol object when
        within another protocol"""
        return instance._data[attribute].get()

    @staticmethod
    def _set(attribute, instance, value, cls, **kwargs):
        """This method defines the way by which this protocol is set when
        within another protocol as an attribute"""
        instance._data[attribute] = instance._data[attribute].set(value,
                                                                  cls=cls)

    @classmethod
    def array(cls, size):
        """Dynamically generate and initialize an array type for the protocol"""
        assert isinstance(size, int)

        class Array(Protocol):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.size = size
                self.data = tuple((cls() for _ in range(size)))

            def __getitem__(self, item):
                return self.data[item].get()

            def __setitem__(self, key, value):
                self.data[key].set(value, cls=cls)

            def __len__(self):
                return self.size

            def calcsize(self, *args, **kwargs):
                size = super().calcsize(*args, **kwargs)
                for d in self.data:
                    size += d.calcsize(*args, **kwargs)
                return size

            def pack_into(self, buffer, offset, *args, **kwargs):
                offset = super().pack_into(buffer, offset, *args, **kwargs)
                for d in self.data:
                    offset = d.pack_into(buffer, offset, *args, **kwargs)
                return offset

            def set(self, value, **kwargs):
                data = tuple((cls().set(v, cls=cls) for v in value))
                if len(data) != len(self):
                    # TODO: make an appropriate exception class
                    raise ValueError('')
                self.data = data
                return self
        return Array


class BaseType(Protocol):
    @property
    def _type(self):
        raise NotImplementedError('')  # TODO: Add indicative message

    def __init__(self):
        super().__init__()
        self.data = self._type()

    def get(self, **kwargs):
        return self.data.value

    def set(self, value, **kwargs):
        self.data.value = value
        return self


class BaseCType(BaseType):
    @property
    def _type(self):
        raise NotImplementedError('')  # TODO: Add indicative message

    @property
    def _fmt(self):
        raise NotImplementedError('')  # TODO: Add indicative message

    def calcsize(self, *args, **kwargs):
        size = super().calcsize(*args, **kwargs)
        return size + struct.calcsize(self._fmt)

    def pack_into(self, buffer, offset, *args, **kwargs):
        offset = super().pack_into(buffer, offset, *args, **kwargs)
        struct.pack_into(self._fmt, buffer, offset, self.data.value)
        return offset + struct.calcsize(self._fmt)


class Char(BaseCType):
    @property
    def _type(self):
        return ctypes.c_char

    @property
    def _fmt(self):
        return 'c'


class Short(BaseCType):
    @property
    def _type(self):
        return ctypes.c_short

    @property
    def _fmt(self):
        return 'h'
