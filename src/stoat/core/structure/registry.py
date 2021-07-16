"""The registry module

This module supplies the bookkeeping functionality that enables the
system to keep coherence between identical classes used in different
places and to prevent the generation of too many classes.
"""
import uuid as uid

_registry = {}


class NoneType:
    pass


def normalize_bases(bases):
    return tuple(
        get_base(b.__blueprint__.uuid)
        for b in bases if hasattr(b, '__blueprint__')
    )


def get_base(uuid, default=NoneType):
    if default is NoneType or uuid in _registry:
        return _registry[uuid]['base']
    else:
        return default


def new_base(uuid, cls):
    _registry[uuid] = {}
    _registry[uuid]['base'] = cls


def get(uuid, config, default=NoneType):
    if default is NoneType:
        return _registry[uuid][config]
    else:
        return _registry[uuid].get(config, default)


def new(uuid, config, cls):
    _registry[uuid][config] = cls
    return cls


def start_transaction():
    return RegisterBaseContext()


class RegisterBaseContext:
    def __init__(self):
        self._uuid = uid.uuid4()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    @property
    def uuid(self):
        return self._uuid

    def new_base(self, cls):
        new_base(self.uuid, cls)
