from .request import Request


class Context:
    """Context class is a data courier for partial structures

    Structures that requires additional information that might only be
    available after class initialization, announces this fact by
    returning a context instance with requests for that information.
    An example for this behavior is dynamic arrays. Static arrays will
    function in the same way to simplify the implementation and keep
    consistency.
    """
    def __init__(self, item, context):
        self.item = item
        self.context = context
