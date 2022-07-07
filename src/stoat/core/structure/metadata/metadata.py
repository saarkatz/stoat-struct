class Metadata:
    def __init__(self, dtype, value, once=False):
        self.dtype = dtype
        self.value = value
        self.once = once

    def merge(self, other):
        raise NotImplementedError('merge not implemented')
