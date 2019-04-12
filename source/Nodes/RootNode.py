"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.ScopedNode import ScopedNode


class RootNode(ScopedNode):
    """
    The root of our program. Root is a ScopedNode, the base scope of our C program.
    """
    _label = "Root"

    def __init__(self):
        super().__init__()
