from .ref import Ref


class This(Ref):
    def __repr__(self):
        return f'This({", ".join(self._path)})'
