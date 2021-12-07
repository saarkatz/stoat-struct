class Metadata:
    def __init__(self, dtype, value):
        self.dtype = dtype
        self.value = value

    def merge(self, other):
        raise NotImplementedError('merge not implemented')
