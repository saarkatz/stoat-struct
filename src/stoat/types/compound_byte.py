from functools import partial
from stoat.core import Structure


class TinyField:
    def __init__(self, size):
        self.size = size
        self._value = 0
        self.maximum = 2 ** self.size

    def check_value(self, value):
        return 0 <= value < self.maximum

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if not self.check_value(value):
            raise ValueError('value out of range for tiny field, expected '
                             '{{0-{mx}}}, got {val}'.format(mx=self.maximum - 1,
                                                            val=value))
        self._value = value


class CompoundByte(Structure):
    def __init__(self, slices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        slices = list(slices)
        # Make sure that we have at most a single byte
        if sum(slices) > 8:
            raise ValueError('the slice given to CompoundByte must be at most a'
                             ' single byte')
        elif sum(slices) < 8:
            slices.append(8 - sum(slices))

        self.slices = slices
        self.parts = []
        for size in slices:
            self.parts.append(TinyField(size))

    def calcsize(self, *args, **kwargs):
        size = super().calcsize(*args, **kwargs)
        return size + 1

    def pack_into(self, buffer, offset, *args, **kwargs):
        offset = super().pack_into(buffer, offset, *args, **kwargs)
        byte = 0
        for i, part in enumerate(self.parts):
            byte |= part.value << sum(self.slices[i + 1:])
        buffer[offset] = byte
        return offset + 1

    @classmethod
    def unpack_from(cls, buffer, offset, *args, **kwargs):
        result, offset = super().unpack_from(buffer, offset, *args, **kwargs)
        assignment = result._set(buffer[offset])
        if not assignment:
            assignment = result
        return assignment, offset + 1

    def _set(self, value, **kwargs):
        # TODO: Handle errors better
        base_mask = 0b11111111
        error = None
        if isinstance(value, (bytes, bytearray)):
            value = value[0]
        try:
            # Assume that the input is a single byte
            for i, size in enumerate(self.slices):
                self.parts[i].value = (value & (
                        base_mask >> sum(self.slices[:i]))) >> sum(
                    self.slices[i + 1:])
        except TypeError as e:
            # Assume that the input is an array of integers
            try:
                assert len(value) == len(self.parts)
                for i, item in enumerate(value):
                    self.parts[i].value = item
            except AssertionError as a:
                error = a
            except ValueError as o:
                # ValueError here means that it is an array but not of
                # integers of inappropriate size
                try:
                    return super()._set(value, **kwargs)
                except TypeError:
                    error = o
            except TypeError as u:
                # TypeError here will occur if value isn't a list or a list
                # of non integer types.
                try:
                    len(value)
                except TypeError:
                    error = e
                else:
                    error = u
        if error:
            raise error

    def __getitem__(self, item):
        return self.parts[item].value

    def __setitem__(self, key, value):
        self.parts[key].value = value
