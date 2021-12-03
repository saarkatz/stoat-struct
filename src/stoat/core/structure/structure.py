from .base import Base


class Structure(Base):
    """Structure is the base class for all structures

    Inherit Structure to implement a  custom structure, either based or
    not based on other structures.
    """
    @classmethod
    def array(cls, size):
        raise Exception('No!')
