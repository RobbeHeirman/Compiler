"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.ExpressionNode import ExpressionNode
from source.Nodes.ScopedNode import ScopedNode


class RootNode(ScopedNode):
    """
    The root of our program. Root is a ScopedNode, the base scope of our C program.
    """
    label = "Root"

    def __init__(self):
        super(ScopedNode, self).__init__()
