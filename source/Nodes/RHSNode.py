"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from source.Nodes.ExpressionNode import ExpressionNode
from source.Specifiers import Operator


class RHSNode(ExpressionNode):
    _operator: Operator

    def __init__(self, parent_node: ExpressionNode, **kwargs):
        super().__init__(parent_node)

        self._operator = kwargs.get('operator', Operator.DEFAULT)
        self._neg = kwargs.get("negative", False)

    def generate_llvm(self):
        print("im called")
        if len(self._children) == 1:
            print("??")
            return self._children[0].generate_llvm()

        if len(self._children) == 2:
            print("yay")

    @property
    def label(self):
        if self._neg:
            return '"* -1"'

        return '"{0}"'.format(self._operator.value)
