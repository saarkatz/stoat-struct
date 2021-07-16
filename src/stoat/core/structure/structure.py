from .base import Base
from .context import Context, ConstRef


class Structure(Base):
    """Structure is the base class for all structures

    Inherit Structure to implement a  custom structure, either based or
    not based on other structures.
    """
    @classmethod
    def array(cls, size):
        if isinstance(size, int):
            size = ConstRef(size)

        return Context(cls, [size])
