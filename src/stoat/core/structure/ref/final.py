from .ref import Ref


class Final(Ref):
    def getattr(self, item):
        raise Exception(f"{self.__class__.__name__} ref can't be extended further.")
