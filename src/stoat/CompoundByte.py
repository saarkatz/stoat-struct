from functools import partial
from stoat.Structure import Structure


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


ATTRIBUTES = ('_accessor_target', '_accessor_key')


class Accessor(type):
    def __new__(mcs, target, *args):
        dictionary = dict()
        for attribute in dir(target):
            if attribute.startswith('_'):
                continue
            value = getattr(target, attribute)
            if callable(value):
                dictionary[attribute] = partial(value, *args)
            else:
                dictionary[attribute] = property(
                    lambda s: getattr(target, attribute),
                    lambda s, v: setattr(target, attribute, v))
        result = super().__new__(mcs, 'Accessor', tuple(), dictionary)
        return result()


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
        if kwargs.get('shallow', False):
            return
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
        if assignment:
            assignment = result
        return assignment, offset + 1

    def _set(self, value, **kwargs):
        base_mask = 0b11111111
        self.parts = []
        if isinstance(value, (bytes, bytearray)):
            value = value[0]
        try:
            for i, size in enumerate(self.slices):
                self.parts.append(TinyField(size))
                self.parts[-1].value = (value & (
                            base_mask >> sum(self.slices[:i]))) >> sum(
                    self.slices[i + 1:])
        except ValueError as e:
            try:
                return super()._set(value, **kwargs)
            except TypeError:
                raise e

    def __getitem__(self, item):
        return self.parts[item].value

    def __setitem__(self, key, value):
        self.parts[key].value = value


if __name__ == '__main__':
    class Test(Structure):
        cb1 = CompoundByte + (1, 2, 3)
        cb2 = CompoundByte + (1, 2, 3, 2)
        cb3 = CompoundByte + [4]


    t = Test()
    t.cb1[0] = 1
    t.cb1[1] = 3
    t.cb1[2] = 7
    t.cb1[3] = 3
    t.cb2 = b'\xda'
    t.cb3 = 129

    print(t.pack())
    print('-'.join((bin(v)[2:] for v in t.pack())))
