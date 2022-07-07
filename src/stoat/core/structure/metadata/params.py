from .metadata import Metadata


class Params(Metadata):
    def __init__(self, value):
        super().__init__('params', value)

    def merge(self, other):
        assert self.dtype == other.dtype
        for key, value in other.value.items():
            if key in self.value:
                raise Exception()  # TODO: Which exception or maybe warning
            self.value[key] = value
