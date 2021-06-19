from abc import ABCMeta
from collections import OrderedDict, namedtuple

from .accessor import Accessor
from .constructor import Constructor
from .partial import Partial
from .registry import registry
from ..configuration import Config


def ref_vars_func(struct):
    return struct.__blueprint__.struct


def data_vars_func(inst):
    return inst.__instane__.data


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
        for key, item in constructor.fields:
            if isinstance(item, Partial):
                context[key] = Partial.context
                item = Partial.item
            if isinstance(item, mcs):
                struct[key] = item
                dictionary[key] = Accessor(key, item, data_vars_func)
            else:
                dictionary[key] = item

        # Normalize the bases
        bases = registry.normalize_bases(bases)

        del dictionary['__blueprint__']
        del dictionary['__config__']
        base = super().__new__(mcs, name, bases, dictionary)

        with registry.start_new() as new:
            base.__config__ = config
            base.__blueprint__ = Blueprint(new.uuid, struct, context)
            new.new_base(base)

        return base.configure(config)

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
        config = cls.__config__(config)
        result = registry.get(uuid, config, None)
        if result:
            return result
        else:
            base = registry.get_base(uuid)
            return registry.new(uuid, config,
                super().__new__(Meta, base.__name__, (base,), {
                    '__config__': config,
                })
            )

