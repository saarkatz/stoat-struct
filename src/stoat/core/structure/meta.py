from abc import ABCMeta
from collections import OrderedDict, namedtuple

from .auto_decorator import register_auto_decorator
from . import registry
from .accessor import Accessor
from .constructor import Constructor
from .context import Context
from ..configuration import Config, Factory


# Register auto decoration
register_auto_decorator()


def ref_vars_func(struct):
    return struct.__blueprint__.struct


def data_vars_func(inst, key):
    return inst.__instance__.data[key]


Blueprint = namedtuple(
    'Blueprint',
    [
        'uuid',
        'struct',
        'context',
    ]
)


class Meta(ABCMeta):
    """Meta is where the magic happens

    This class is the metaclass connecting together all the magic needed to
    implement the stoat system.
    Some of said magic is implemented here and some more is implemented in the
    Constructor class.
    """
    @classmethod
    def __prepare__(metacls, name, bases):
        return Constructor(metacls, name, bases, ref_vars_func)

    def __new__(mcs, name, bases, constructor):
        dictionary = {}
        context = {}
        struct = OrderedDict()

        # Get the config
        config = Config(constructor.fields.get('__config__', {}))
        dictionary['config'] = config.builder()

        # Collect all the members
        for key, item in constructor.fields.items():
            if isinstance(item, Context):
                context[key] = item.context
                item = item.item
            if isinstance(item, mcs):
                struct[key] = item
                dictionary[key] = Accessor(key, item, data_vars_func)
            else:
                dictionary[key] = item

        # Normalize the bases
        bases = registry.normalize_bases(bases)

        dictionary.pop('__blueprint__', None)
        dictionary.pop('__config__', None)
        base = super().__new__(mcs, name, bases, dictionary)

        with registry.start_transaction() as new:
            base.__config__ = config
            base.__blueprint__ = Blueprint(new.uuid, struct, context)
            new.new_base(base)

        return base

    def __auto_decorator__(cls):
        return cls.configure(cls.config)

    # Fix isinstance  for Structure classes
    def __instancecheck__(self, instance):
        return type.__instancecheck__(
            registry.get_base(self.__blueprint__.uuid), instance
        )

    # Fix issubclass for Structure classes
    def __subclasscheck__(self, subclass):
        return type.__subclasscheck__(
            registry.get_base(self.__blueprint__.uuid), subclass
        )

    # Square bracket operator -> Create array
    def __getitem__(cls, size):
        return cls.array(size)

    # Classes generated through configuration change will be looked for in the
    # dictionary
    def __lt__(cls, config):
        return cls.configure(config)

    def array(cls, size):
        raise NotImplementedError(
            "Array method not implemented for type {}".format(cls.__name__))

    def configure(cls, config):
        uuid = cls.__blueprint__.uuid
        if isinstance(config, Factory):
            config = cls.__config__(config.get())
        else:
            config = cls.__config__(config)
        result = registry.get(uuid, config, None)
        if result:
            return result
        else:
            base = registry.get_base(uuid)

            dictionary = {}
            name = f'c{hash(config)}'
            qualname = '.'.join((base.__qualname__, name))
            dictionary['__module__'] = base.__module__
            dictionary['__qualname__'] = qualname
            dictionary['__config__'] = config
            if hasattr(base, '__doc__'):
                dictionary['__doc__'] = base.__doc__

            return registry.new(uuid, config,
                super().__new__(Meta, name, (base,), dictionary)
            )
