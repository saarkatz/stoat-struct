"""
In this module the group structure is defined.
The sole purpose of the group structure is to allow for grouping when
defining structures. This is only needed to allow for referencing values
outside the group.
"""
from stoat.core.base_structure import BaseStructure


class Section(BaseStructure):
    def __init__(self, _parent):
        assert _parent
        super().__init__(_parent=_parent)

    @classmethod
    def array(cls, size):
        raise Exception('Structure sections can\'t be used directly in an array')
