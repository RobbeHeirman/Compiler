"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.ExpressionNode import ExpressionNode


class PostFixNode(ExpressionNode):
    label = "PostFix"

    def __init__(self, parent_node):
        super().__init__(parent_node)
