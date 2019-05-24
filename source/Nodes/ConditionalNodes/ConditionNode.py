"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Specifiers import ConditionalOperator


class ConditionNode(ExpressionNode):

    def __init__(self, parent_node, operator):
        super().__init__(parent_node)

        self._type = ConditionalOperator(operator)

    @property
    def label(self):
        return self._type.value