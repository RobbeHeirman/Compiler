"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Specifiers import ConditionType


class IfElseNode(ExpressionNode):

    def __init__(self, parent_node, c_type: ConditionType):
        super().__init__(parent_node)

        self._cond_type = c_type

    @property
    def label(self):
        return self._cond_type.value
