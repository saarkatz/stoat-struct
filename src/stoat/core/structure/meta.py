from abc import ABCMeta
from collections import OrderedDict, namedtuple

from .constructor import Constructor
from .accessor import Accessor
from .ref import This

Blueprint = namedtuple(
    'Blueprint',
    [
        'shape',
    ]
)


class Meta(ABCMeta):
    @classmethod
    def __prepare__(metacls, name, bases):
        return Constructor(name)

    def __new__(mcs, name, bases, constructor):
        shape = OrderedDict()
        dictionary = constructor.fields
        annotations = dictionary.pop('__annotations__', {})

        for field, struct in annotations.items():
            if isinstance(struct, (Meta, This)):
                shape[field] = [struct, None]

        ref_fields = []
        for field in shape.keys():
            if isinstance(shape[field], This):
                ref_fields.append(field)
            shape[field][1] = dictionary.get(field, None)
            annotations.pop(field)

        for field in ref_fields:
            shape[field] = mcs.query_ref(shape, field)

        # TODO: Construct the dependency graph of the structure

        # TODO: Some relatively complicated logic to verify that there are no loops in the structure

        # Set the fields of the structure to properties
        for field, struct in shape.items():
            dictionary[field] = Accessor(shape[field][0], field)

        dictionary['__annotations__'] = annotations
        dictionary['__blueprint__'] = Blueprint(shape=shape)
        return super().__new__(mcs, name, bases, dictionary)

    @classmethod
    def query_ref(mcs, shape, field, prev=None):
        ref = shape[field]
        if not isinstance(ref, This):
            return ref
        if not ref._path:
            raise Exception('Self reference.')
        item = shape[ref._path[0]][0]
        if item in prev:
            raise Exception('Loop!')
        else:
            item = mcs.query_ref(shape, item, prev + [ref])
            shape[ref._path[0]][0] = item
        return item._query_ref(ref.__class__(ref._path[1:]))

    def _query_ref(cls, ref, prev=None):
        if not ref._path:
            return cls
        item = cls.__blueprint__.shape[ref._path[0]][0]
        if isinstance(item, This):
            prev = prev if prev else []
            if item in prev:
                raise Exception('Loop!')
            else:
                item = cls._query_ref(item, prev + [ref])
                cls.__blueprint__.shape[ref._path[0]][0] = item
        return item._query_ref(ref.__class__(ref._path[1:]))

    def array(cls, size):
        raise NotImplementedError(
            "Array method not implemented for type {}".format(cls.__name__))

    @classmethod
    def dynamic(mcs, name, bases, dictionary, fields):
        constructor = mcs.__prepare__(name, bases)
        constructor.fields = dictionary
        constructor.fields['__annotations__'] = fields
        return mcs.__new__(mcs, name, bases, constructor)
