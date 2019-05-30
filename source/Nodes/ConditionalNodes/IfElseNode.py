"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from Nodes.AbstractNodes.ScopedNode import ScopedNode
from Specifiers import ConditionType


class IfElseNode(ScopedNode):

    def __init__(self, parent_node, c_type: ConditionType):
        super().__init__(parent_node)

        self._cond_type = c_type

    @property
    def label(self):
        return self._cond_type.value
