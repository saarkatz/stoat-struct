from abc import ABCMeta, abstractmethod

from ._accessor import Accessor
from ._constructor import Constructor
from ._registry import Registry


class Meta(ABCMeta):
    """Meta is where the magic happens

    This class is the metaclass connecting together all the magic needed to
    implement the stoat system.
    Some of said magic is implemented here and some more is implemented in the
    Constructor class.
    """
    @classmethod
    def __prepare__(metacls, name, bases):
        pass

    def __new__(cls, *args, **kwargs):
        pass
