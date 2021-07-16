import builtins
from threading import Lock

registering = False
registered = False

_orig_build_class = None

__AUTO_DECORATOR__ = '__auto_decorator__'


mutex = Lock()


def noop(cls):
    return cls


def register_auto_decorator():
    global registering
    global registered

    if registered or registering:
        return
    mutex.acquire()
    if registered or registering:
        mutex.release()
        return
    registering = True
    mutex.release()

    global _orig_build_class
    _orig_build_class = orig_build_class = builtins.__build_class__

    # Extend metaclass funtionality with __auto_decorator__
    def auto_decorator_build_class(func, name, *bases, **kwargs):
        # Get the instance of the class type
        instance = orig_build_class(func, name, *bases, **kwargs)

        # Capitalizing on the metaclass search done in __build_class__ the
        # final result is the real meta class used for the type
        meta = type(instance)
        decorator = getattr(meta, __AUTO_DECORATOR__, noop)

        # Return the decorated type
        return decorator(instance)

    builtins.__build_class__ = auto_decorator_build_class
    registered = True
    registering = False


def unregister_auto_decorator():
    global registering
    global registered

    if not registered or registering:
        return
    mutex.acquire()
    if not registered or registering:
        mutex.release()
        return
    registering = True
    mutex.release()

    global _orig_build_class

    builtins.__build_class__ = _orig_build_class

    _orig_build_class = None
    registered = False
    registering = False

