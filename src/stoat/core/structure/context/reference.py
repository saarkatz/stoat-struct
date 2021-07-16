def finalize(ref):
    ref._Reference__finalize()


def get_target(ref):
    return ref._Reference__target


class Reference:
    """Reference tracks referenced classes within a structure

    This class is used within the Constructor to track references
    required by structure field to other structure fields within the new
    structure class.
    This way the reference class represents a coupling between data and
    structure.
    """
    pass


class ConstRef(Reference):
    def __init__(self, value):
        self.value = value


class ForwardRef(Reference):
    def __init__(self, target_type, target, name, vars_func, _path=None):
        self.__type = target_type
        self.__target = target
        self.__path = _path if _path else []
        self.__is_finalized = False

        self._Reference__path.append(name)

        # Build path options
        self.__path_options = {}
        for key, item in vars_func(target):
            if key.startswith('_'):
                continue
            if isinstance(item, target_type):
                self._Reference__path_options[key] = item

    def __finalize(self):
        self._Reference__is_finalized = True

    def __getattr__(self, item):
        if self._Reference__is_finalized:
            if item == 'path':
                return self._Reference__path
            if item == 'target':
                return self._Reference__target
            if item == 'type':
                return self._Reference__type
            raise AttributeError(
                f"'Reference' object has no attribute '{item}'"
            )
        else:
            if item in self._Reference__path_options:
                return ForwardRef(
                    self._Reference__type,
                    self._Reference__path_options[item],
                    item,
                    self._Reference__path,
                )
            else:
                raise AttributeError(
                    "Referenced '{}' object has no attribute '{}' of type '{}'"
                    .format(
                        self._Reference__target.__name__,
                        item,
                        self._Reference__type.__name__,
                    )
                )
