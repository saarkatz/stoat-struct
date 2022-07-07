from abc import ABCMeta
from collections import OrderedDict, namedtuple

from .constructor import Constructor
from .accessor import Accessor
from .metadata import Metadata
from .ref import This


Blueprint = namedtuple(
    'Blueprint',
    [
        'shape',
        'metadata',
    ]
)


class Meta(ABCMeta):
    @classmethod
    def __prepare__(metacls, name, bases):
        return Constructor(name)

    def __new__(mcs, name, bases, constructor):
        shape = OrderedDict()
        metadata = {}
        dictionary = constructor.fields
        annotations = dictionary.pop('__annotations__', {})

        # Collect all the fields and their metadata
        ref_fields = []
        for field, struct in annotations.items():
            if isinstance(struct, (Meta, This)):
                shape[field] = struct
                metadata[field] = mcs.construct_metadata(dictionary.pop(field, None))
            if isinstance(shape[field], This):
                ref_fields.append(field)

        # Pop all the fields from the annotations TODO: Add back in automatic annotation for the fields
        for field in shape.keys():
            annotations.pop(field)

        for field in ref_fields:
            shape[field] = mcs.query_ref(shape, field)

        # TODO: Construct the dependency graph of the structure

        # TODO: Some relatively complicated logic to verify that there are no loops in the structure

        # Set the fields of the structure to properties
        for field, struct in shape.items():
            dictionary[field] = Accessor(field, shape[field])

        dictionary['__annotations__'] = annotations
        dictionary['__blueprint__'] = Blueprint(shape=shape, metadata=metadata)
        return super().__new__(mcs, name, bases, dictionary)

    @classmethod
    def construct_metadata(mcs, data):
        metadata = {}
        if data is None:
            return metadata
        if isinstance(data, (tuple, list)):
            for d in data:
                if d.dtype in metadata:
                    if d.once:
                        raise Exception(f"{d.dtype} can only appear once")
                    metadata[d.dtype].merge(d)
                else:
                    metadata[d.dtype] = d
        elif isinstance(data, Metadata):
            metadata[data.dtype] = data
        return {dtype: d.value for dtype, d in metadata.items()}

    @classmethod
    def query_ref(mcs, shape, field, prev=None):
        ref = shape[field]
        if not isinstance(ref, This):
            return ref
        if not ref._path:
            raise Exception('Self reference.')
        item = shape[ref._path[0]]
        if item in prev:
            raise Exception('Loop!')
        else:
            item = mcs.query_ref(shape, item, prev + [ref])
            shape[ref._path[0]] = item
        return item._query_ref(ref.__class__(ref._path[1:]))

    def _query_ref(cls, ref, prev=None):
        if not ref._path:
            return cls
        item = cls.__blueprint__.shape[ref._path[0]]
        if isinstance(item, This):
            prev = prev if prev else []
            if item in prev:
                raise Exception('Loop!')
            else:
                item = cls._query_ref(item, prev + [ref])
                cls.__blueprint__.shape[ref._path[0]] = item
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
