from collections import namedtuple
from enum import Enum, auto

from .conditions import ListCondition


Rule = namedtuple('Rule', ['condition', 'type'])


class ItemType(Enum):
    List = auto()
    Value = auto()


class NoneType:
    pass


def get_item_from_list(item, lst):
    for i in lst:
        if (
            item == i
            or (hasattr(i, '__name__') and item == i.__name__)
            or (hasattr(i, 'name') and item == i.name)
            or item == str(i)
        ):
            return i
    return NoneType


class Builder:
    def __init__(self, factory, name, rule):
        self._factory = factory
        self._name = name
        self._rule = rule

    def __getattr__(self, item):
        if self._rule.type is ItemType.List:
            i = get_item_from_list(item, self._rule.condition.values)
            if i is not NoneType:
                self._rule.condition.validate(i)
                self._factory.set(self._name, i)
                return self._factory
        raise AttributeError(f"'{self._name}' has no possible value '{item}'")

    def __call__(self, item):
        self._rule.condition.validate(item)
        self._factory.set(self._name, item)
        return self._factory


class Factory:
    def __init__(self, config=None):
        self._config = config
        self._rules = {}
        self._data = {}
        self.is_active = False

    def add_rule(self, key, condition):
        self._rules[key] = Builder(self, key, Rule(
            condition,
            ItemType.List if isinstance(condition, ListCondition) else ItemType.Value
        ))

    def __getattr__(self, item):
        if not self.is_active:
            active_copy = Factory(self._config)
            if active_copy._config:
                for key, condition in active_copy._config.conditions.items():
                    active_copy.add_rule(key, condition)
            active_copy.is_active = True
            return getattr(active_copy, item)

        if item in self._rules:
            return self._rules[item]
        raise AttributeError(f"Configuration has no key '{item}'")

    def set(self, key, value):
        if self.is_active:
            self._data[key] = value

    def get(self):
        return self._data
