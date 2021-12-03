import re


item_pattern = re.compile('[_a-zA-Z][_a-zA-Z0-9]*')


class Ref:
    def __init__(self, initial_path=None):
        self._path = initial_path if initial_path else []

    def __getattr__(self, item):
        if item.startswith('_'):
            raise Exception('Access to private members is only allowed through the _private accessor.')
        return self.getattr(item)

    def _private(self, item):
        return self.getattr('_' + item)

    def getattr(self, item):
        assert item_pattern.fullmatch(item), 'An item must be a valid python attribute name'
        return Ref(initial_path=self._path + [item])

    def __repr__(self):
        return f'Ref({", ".join(self._path)})'
