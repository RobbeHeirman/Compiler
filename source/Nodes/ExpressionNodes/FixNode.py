"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from enum import Enum

from Nodes.AbstractNodes.NonLeafNode import NonLeafNode


class FixType(Enum):
    ARRAY = "[]"
    FUNCTION = "()"
    PTR = "*"
    ADDRESS = "&"


class FixNode(NonLeafNode):

    def __init__(self, parent_node, f_type: FixType):
        super().__init__(parent_node)
        self.f_type = f_type
        self.rhs_node = None

    @property
    def label(self):
        return self.f_type.value

    def add_child(self, child):
        self.rhs_node = child
        super().add_child(child)
