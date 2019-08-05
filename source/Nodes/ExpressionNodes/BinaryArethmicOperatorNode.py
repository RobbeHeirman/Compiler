"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from enum import Enum

from Nodes.ExpressionNodes.BinaryExpressionNode import BinaryExpressionNode


class Operator(Enum):
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIVIDE = '/'


class BinaryArethmicOperatorNode(BinaryExpressionNode):

    @property
    def llvm_value(self) -> str:
        return ""

    def __init__(self, parent_node, ctx):
        super().__init__(parent_node, ctx)
        self._operator = Operator(ctx.getChild(1).getText())

    @property
    def label(self):
        return self._operator.value
