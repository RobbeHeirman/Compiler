"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from antlr4 import ParserRuleContext

from source.Nodes.ExpressionNode import ExpressionNode
from source.Specifiers import Operator


class RHSNode(ExpressionNode):

    _operator: Operator

    def __init__(self, parent_node, operator: Operator = Operator.DEFAULT):
        super().__init__(parent_node)

        self._operator = operator

    def llvm_code_value(self):
        pass

    @property
    def label(self):
        return '"{0}"'.format(self._operator.value)
