from .metadata import Metadata


class Default(Metadata):
    def __init__(self, value):
        super().__init__("default", value, True)

    def merge(self):
        raise Exception()  # TODO: default can only be used once and therefore cant be merged
