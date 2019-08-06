"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import Nodes.AbstractNodes.ScopedNode as ScopedNode
from Specifiers import ConditionType


class IfElseNode(ScopedNode.ScopedNode):

    def __init__(self, parent_node, ctx, c_type: ConditionType):
        super().__init__(parent_node, ctx)

        self._cond_type = c_type

    @property
    def label(self):
        return self._cond_type.value
