from .meta import Meta


class Base(metaclass=Meta):
    """Base is base class for the Structure class and Array class

    This class is required to prevent circular import between Structure
    and Array.
    """
    pass
