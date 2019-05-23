"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from antlr4 import ParserRuleContext

from Nodes.AbstractNodes.ExpressionNode import ExpressionNode


class PtrNode(ExpressionNode):
    label = "*"

    def __init__(self, parent_node):
        super().__init__(parent_node)
