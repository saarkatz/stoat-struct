class Accessor(property):
    """Accessor is a property factory for structure fields

    The Accessor is used by the Meta metaclass to generate accessors for the
    structure fields inside a new strcuture class.
    """
    def __init__(self, key, item):
        super().__init__(
            lambda s: item.getter(s.__instance__.data[key]),
            lambda s, v: item.setter(s.__instance__.data[key], v),
        )
