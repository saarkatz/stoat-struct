from abc import ABC, abstractmethod


class Condition(ABC):
    @abstractmethod
    def validate(self, value):
        pass

    @property
    @abstractmethod
    def default(self):
        pass
