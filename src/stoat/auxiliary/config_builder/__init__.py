"""
The configuration builder is an auxiliary module for generating configuration
dictionaries.
"""
from enum import Enum, auto


class ItemType(Enum):
    Enum = auto()
    Value = auto()


class Item:
    def __init__(self, name, access_name, item_type):
        self.name = name
        self.access_name = access_name if access_name else name
        self.item_type = item_type


class EnumItem(Item):
    def __init__(self, name, access_name, enum):
        super().__init__(name, access_name, ItemType.Enum)
        self.enum = enum


class ValueItem(Item):
    def __init__(self, name, access_name):
        super().__init__(name, access_name, ItemType.Value)


class ConfigBuilder:
    def __init__(self, items):
        self.items = {i.access_name: i for i in items}
        self.is_loaded = False
        self.context = None
        self.result = {}

    def add_item(self, item):
        if not self.is_loaded:
            self.items.update({item.access_name: item})

    def __getattribute__(self, item):
        if item in ["is_loaded", "items", "context", "result", "add_item", "bake", "__class__"]:
            return super().__getattribute__(item)

        if not self.is_loaded:
            if item in self.items:
                builder = ConfigBuilder(self.items.values())
                builder.is_loaded = True
                builder.context = builder
                return getattr(builder, item)
            else:
                super().__getattribute__(item)
        else:
            if isinstance(self.context, EnumItem) and item in self.context.enum.__members__:
                self.result.update({self.context.name: getattr(self.context.enum, item)})
                self.context = self
                return self
            elif self.context is self and item in self.context.items:
                self.context = self.context.items[item]
                return self
            else:
                super().__getattribute__(item)

    def __call__(self, value):
        if self.is_loaded:
            if isinstance(self.context, ValueItem):
                self.result.update({self.context.name: value})
                self.context = self.source.root_context
                return self
            else:
                return self.result.copy()

    def bake(self):
        return self.result
