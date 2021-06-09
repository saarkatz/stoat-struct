class Registry:
    """Registry class responsible for structure bookkeeping

    This class is responsible for identifying structure classes generated
    through the system. This is used both to prevent regeneration of the same
    classes multiple times as well as to ensure that different instances of the
    same class will behave nicely when used within isinstance and issubclass
    """
    pass
