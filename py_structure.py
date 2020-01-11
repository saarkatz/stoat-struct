"""
This module defines the infrastructure for the simple definition of binary
protocols.
Requires python >= 3.6
"""
import ctypes
import struct as Struct
from functools import partial
from collections import OrderedDict


class BaseStructureException(Exception):
    pass


class AbstractMethodException(BaseStructureException):
    pass  # TODO: Consider using ABC


class StructureViolationError(BaseStructureException):
    pass


class StructSyntaxError(BaseStructureException):
    pass


def copy_inherited_attribute(cls, base, attr, values,
                             copy_method=dict.copy, update_method=dict.update):
    """
    Sets the attribute attr in cls to a copy of the attribute in base and
    updates it with values. If attr does not exists within base then it will
    contain only values within cls"""
    base_values = getattr(base, attr, None)
    if base_values:
        setattr(cls, attr, copy_method(base_values))
        update_method(getattr(cls, attr), values)
    else:
        setattr(cls, attr, copy_method(values))


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
        brackets.
    """
    def __new__(mcs, name, bases, dictionary):
        result = super().__new__(mcs, name, bases, dictionary)
        base = super(result, result)

        # Inherit _structure
        copy_inherited_attribute(result, base, '_structure',
                                 dictionary.get('_structure', OrderedDict()),
                                 OrderedDict.copy, OrderedDict.update)

        # Inherit _struct_data
        copy_inherited_attribute(result, base, '_struct_data',
                                 dictionary.get('_struct_data', {}))

        for attribute, value in dictionary.items():
            if isinstance(value, MetaProtocol):
                value = result._structure[attribute] = value._prepare(attribute)
                setattr(result, attribute, value.property(attribute))

        return result

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

    def __getitem__(cls, item):
        return cls.array(item)

    def __add__(cls, parameter):
        return cls.parameterized(parameter)

    def __neg__(cls):
        return cls.referenceable()

    def __iter__(self):
        raise BaseStructureException("Type class can't be iterated over!")


class GroundStructInterface(metaclass=MetaProtocol):
    """
    Base interface for all the struct classes.
    Defines all the functions that a complete struct would need to implement
    """
    # INITIALIZATION
    def __init__(self, *args, **kwargs):
        raise AbstractMethodException('')

    # COMMON METHODS
    def calcsize(self, *args, **kwargs):
        """Calculate the size in bytes of the data"""
        raise AbstractMethodException('')

    def pack(self, *args, **kwargs):
        """Pack the data into a binary array"""
        raise AbstractMethodException('')

    def pack_into(self, buffer, offset, *args, **kwargs):
        """Pack the data into a buffer starting at the specified offset"""
        raise AbstractMethodException('')

    @classmethod
    def unpack(cls, buffer, *args, **kwargs):
        """Instantiate the class from the supplied buffer"""
        raise AbstractMethodException('')

    @classmethod
    def unpack_from(cls, buffer, offset, *args, **kwargs):
        """Instantiate the class from the supplied buffer starting at offset"""
        raise AbstractMethodException('')

    # FIELD DATA GETTERS AND SETTERS
    def get(self, **kwargs):
        """Get the data containing object"""
        raise AbstractMethodException('')

    def set(self, value, cls, **kwargs):
        """Set the data. This method should return the updated object"""
        raise AbstractMethodException('')

    @staticmethod
    def _get(attribute, instance, **kwargs):
        """Get the object from its containing type"""
        raise AbstractMethodException('')

    @staticmethod
    def _set(attribute, instance, value, cls, **kwargs):
        """Set the object within its containing type"""
        raise AbstractMethodException('')

    # REQUIRED CLASS METHODS
    @classmethod
    def _prepare(cls, attribute, *args, **kwargs):
        """
        Setup the type within the structure. Returns the final class.
        Called when the type is about to be initialized in another
        structure class.
        """
        raise AbstractMethodException('')

    @classmethod
    def referenceable(cls):
        """Return a type of this class that is referencable"""
        raise AbstractMethodException('')

    @classmethod
    def parameterized(cls, parameter):
        """Return a type of this class with the specified parameter"""
        raise AbstractMethodException('')

    @classmethod
    def array(cls, size):
        """Return an array type with this class for its data"""
        raise AbstractMethodException('')


class BasicGeneralStructure(GroundStructInterface):
    """
    Implement general structure functionality.
    Does not support arraying, referencing and parameterization.
    """
    def __init__(self, *args, **kwargs):
        self._data = OrderedDict()
        self._instance = kwargs.get('_instance', None)
        kwargs['_instance'] = self
        if kwargs.get('shallow', False):
            return
        for field, struct in self._structure.items():
            self._data[field] = struct(*args, **kwargs)
            # if struct._struct_data.get('referencing', False):
            #     self._data[field]._instance = self

    def calcsize(self, *args, **kwargs):
        size = 0
        for data_field in self._data.values():
            size += data_field.calcsize(*args, **kwargs)
        return size

    def pack(self, *args, **kwargs):
        size = self.calcsize()
        binstate = bytearray(size)
        self.pack_into(binstate, 0, *args, **kwargs)
        return bytes(binstate)

    def pack_into(self, buffer, offset, *args, **kwargs):
        for data_field in self._data.values():
            offset = data_field.pack_into(buffer, offset, *args, **kwargs)
        return offset

    @classmethod
    def unpack(cls, buffer, *args, **kwargs):
        result, _ = cls.unpack_from(buffer, 0, *args, **kwargs)
        return result

    @classmethod
    def unpack_from(cls, buffer, offset, *args, **kwargs):
        result = cls(shallow=True, **kwargs)
        kwargs['_instance'] = result
        for field, struct in result._structure.items():
            # if struct._struct_data.get('referencing', False):
            result._data[field], offset = \
                struct.unpack_from(buffer, offset, *args, **kwargs)
            # else:
            #     result._data[field], offset = \
            #         struct.unpack_from(buffer, offset, *args, **kwargs)

        return result, offset

    def get(self, **kwargs):
        return self

    def set(self, value, cls, **kwargs):
        if not isinstance(value, cls):
            raise ValueError(
                "Can't assign data of type '{value}' to field of type "
                "'{source}'".format(value=type(value), source=cls))
        return value

    @staticmethod
    def _get(attribute, instance, **kwargs):
        return instance._data[attribute].get()

    @staticmethod
    def _set(attribute, instance, value, cls, **kwargs):
        instance._data[attribute] = \
            instance._data[attribute].set(value, cls=cls)

    @classmethod
    def _prepare(cls, *args, **kwargs):
        return cls


class Referenceable(BasicGeneralStructure):
    """
    Implements referencing functionality
    """
    @classmethod
    def referenceable(cls):
        class Reference(cls):
            _struct_data = {
                'is_ref': True,
                'reference': None,
            }

            def __init__(self, *args, _instance=None, **kwargs):
                super().__init__(*args, **kwargs)
                self._instance = _instance

            @classmethod
            def _prepare(cls, attribute, *args, **kwargs):
                result = super()._prepare(attribute, *args, **kwargs)
                if result._struct_data.get('reference', None):
                    raise StructureViolationError('Attempting to create two '
                                                  'fields with the same '
                                                  'reference!')
                result._struct_data['reference'] = attribute
                return result

            @classmethod
            def referenceable(cls):
                raise StructSyntaxError("Can't make referenceable a "
                                        "referenceable type. Use only a "
                                        "single dash ('-')!")
        return Reference

"""
        assert isinstance(size, int)

        class Array(Protocol):
            @property
            def _cls(self):
                return cls

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.size = size
                self.data = tuple((self._cls() for _ in range(size)))

            def __getitem__(self, item):
                return self.data[item].get()

            def __setitem__(self, key, value):
                self.data[key].set(value, cls=self._cls)

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
                data = tuple((self._cls().set(v, cls=self._cls) for v in value))
                if len(data) != len(self):
                    # TODO: make an appropriate exception class
                    raise ValueError('')
                self.data = data
                return self

            @classmethod
            def parametrize(cls, parameter):
                parametrized_cls = cls._cls.fget(None).parametrize(parameter)

                class Parametrized(cls):
                    @property
                    def _cls(self):
                        return parametrized_cls
                return Parametrized

        return Array
"""


class Structure(Referenceable):
    pass


class BaseType(Structure):
    _struct_data = {
        'type': None
    }

    @property
    def _type(self):
        return self._struct_data['type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = self._type()

    def get(self, **kwargs):
        return self.data.value

    def set(self, value, **kwargs):
        self.data.value = value
        return self


class BaseCType(BaseType):
    _struct_data = {
        'fmt': None
    }

    @property
    def _fmt(self):
        return self._struct_data['fmt']

    def calcsize(self, *args, **kwargs):
        size = super().calcsize(*args, **kwargs)
        return size + Struct.calcsize(self._fmt)

    def pack_into(self, buffer, offset, *args, **kwargs):
        offset = super().pack_into(buffer, offset, *args, **kwargs)
        Struct.pack_into(self._fmt, buffer, offset, self.data.value)
        return offset + Struct.calcsize(self._fmt)

    @classmethod
    def unpack_from(cls, buffer, offset, *args, **kwargs):
        result, offset = super().unpack_from(buffer, offset, *args, **kwargs)
        value = Struct.unpack_from(cls._struct_data['fmt'], buffer, offset)[0]
        return (result.set(value),
                offset + Struct.calcsize(cls._struct_data['fmt']))

    @classmethod
    def parametrize(cls, endianness):
        fmt = endianness + cls._struct_data['fmt']  # TODO: Problematic

        class Parametrized(cls):
            _struct_data = {
                'fmt': fmt
            }

            @classmethod
            def parametrize(cls, parameter):
                raise Exception('')  # TODO: Make appropriate exception
        return Parametrized


class Char(BaseCType):
    _struct_data = {
        'type': ctypes.c_char,
        'fmt': 'c'
    }


class Short(BaseCType):
    _struct_data = {
        'type': ctypes.c_short,
        'fmt': 'h'
    }


class RefTest(Structure):
    @classmethod
    def array(cls, size):
        assert issubclass(size, BaseType) and \
               size._struct_data.get('is_ref', False)

        class Test(Structure):
            _struct_data = {
                'referencing': True
            }

            def get_ref(self):
                return self._instance._data[size._struct_data['reference']]

            def get_ref_value(self):
                return getattr(self._instance, size._struct_data['reference'])

            def set_ref_value(self, value):
                setattr(self._instance, size._struct_data['reference'], value)

            def calcsize(self, *args, **kwargs):
                s = super().calcsize(self, *args, **kwargs)
                return s + size.calcsize(self.get_ref(), *args, **kwargs)

            def pack_into(self, buffer, offset, *args, **kwargs):
                offset = super().pack_into(buffer, offset, *args, **kwargs)
                return size.pack_into(self.get_ref(), buffer, offset, *args,
                                      **kwargs)

            @classmethod
            def unpack_from(cls, buffer, offset, *args, **kwargs):
                result, offset = super().unpack_from(buffer, offset, *args,
                                                     **kwargs)
                # result._instance = kwargs['instance']
                return result, offset + size.calcsize(
                    result.get_ref(), *args, **kwargs)

            def get(self, **kwargs):
                return self.get_ref_value()

            def set(self, value, **kwargs):
                self.set_ref_value(value)
                return self
        return Test
