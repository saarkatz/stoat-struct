from collections import namedtuple


Ref = namedtuple('Ref', ['type', 'target', 'path', 'is_finalized'])


def finalize(ref):
    ref._ForwardRef__finalize()


def get_target(ref):
    return ref._ForwardRef__ref.target


class ForwardRef:
    def __init__(self, target_type, target, name, vars_func, _path=None):
        self.__ref = Ref(
            type=target_type,
            target=target,
            path=_path if _path is not None else [],
            is_finalized=[],
        )

        self.__ref.path.append(name)

        # Build path options
        options = {}
        for key, item in vars_func(target):
            if key.startswith('_'):
                continue
            if isinstance(item, target_type):
                options[key] = item

        self.__options = options

    def __finalize(self):
        if not self.__ref.is_finalized:
            self.__ref.is_finalized.append(True)

    def __getattr__(self, item):
        if self.__ref.is_finalized:
            if item in ('path', 'target', 'type'):
                return getattr(self.__ref, item)
            else:
                raise AttributeError(
                    f"'ForwardRef' object has no attribute '{item}'"
                )
        else:
            if item in self.__options:
                return ForwardRef(
                    self.__ref.type,
                    self.__options[item],
                    item,
                    self.__ref.path,
                )
            else:
                raise AttributeError(
                    "Referenced '{}' object has no attribute '{}' of type '{}'"
                    .format(
                        self.__ref.target.__name__,
                        item,
                        self.__ref.type.__name__,
                    )
                )
