from .ref import Ref
from .final import Final


class Param(Final):
    pass


class GetParam(Ref):
    def getattr(self, item):
        self.validate(item)
        return Param(initial_path=[item])
