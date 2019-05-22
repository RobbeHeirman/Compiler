"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.ExpressionNode import ExpressionNode


class RHSFunctionNode(ExpressionNode):
    label = "()"

    def __init__(self, parent_node):
        super().__init__(parent_node)
