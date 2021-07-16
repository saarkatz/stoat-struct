"""
The config module defines the structure responsible for holding data about the
configuration of a structure type.
This is so that make variations of a type that do not require a redefinition
while still keeping each different configuration its own type for correct type
information.
"""
from .builder import Factory
from .conditions.condition import Condition


class Config:
    def __init__(self, conditions):
        if isinstance(conditions, Config):
            self.conditions = conditions.conditions.copy()
            self.dictionary = conditions.dictionary.copy()
        else:
            self.conditions = dict(conditions)
            self.dictionary = {}

            # Validate the conditions
            for condition in self.conditions.values():
                assert isinstance(condition, Condition)

        self._hash = None

    def validate(self, other):
        for key, value in other.items():
            if (key not in self.conditions
                    or not self.conditions[key].validate(value)):
                return False
        return True

    def get(self, key, default=None):
        if key not in self.conditions:
            raise KeyError(key)

        if default:
            return self.dictionary.get(key, default)
        elif self.conditions[key].default:
            return self.dictionary.get(key, self.conditions[key].default)
        else:
            return self.dictionary.get(key)

    def __getitem__(self, item):
        return self.get(item)

    def __call__(self, *args, **kwargs):
        dictionary = dict(*args, **kwargs)
        assert self.validate(dictionary)
        config = Config({})
        config.conditions = self.conditions.copy()
        config.dictionary = dictionary
        return config

    def __eq__(self, other):
        if not isinstance(other, Config):
            return False
        else:
            if set(self.keys()) != set(other.keys()):
                return False
            for key in self.conditions.keys():
                if self.get(key) != other.get(key):
                    return False
            return True

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(sum((hash(str(k)+str(v)) for k, v in self.items())))
        return self._hash

    def keys(self):
        return self.conditions.keys()

    def values(self):
        return (self.get(k) for k in self.keys())

    def items(self):
        return zip(self.keys(), self.values())

    def remove(self, key):
        config = Config({})
        config.conditions = self.conditions.copy()
        config.dictionary = {k: v for k, v in self.dictionary.items() if
                             not k == key}
        return config

    def update(self, __m, **kwargs):
        target = dict(self.dictionary)
        target.update(__m, **kwargs)
        return self(target)

    def default(self):
        return Config(self.conditions.copy())

    def merge(self, other):
        config = Config(self)
        other = Config(other)
        config.conditions.update(other.conditions)
        config.dictionary.update(other.dictionary)
        assert config.validate(config.dictionary)
        return config

    def builder(self):
        return Factory(self)
