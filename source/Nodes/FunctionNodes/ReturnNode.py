"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from Nodes.AbstractNodes.ExpressionNode import ExpressionNode
from Specifiers import TypeSpecifier


class ReturnNode(ExpressionNode):
    label = "return"

    def __init__(self, parent_node: ExpressionNode):
        super().__init__(parent_node)

    @property
    def base_type(self):
        return TypeSpecifier.DEFAULT
