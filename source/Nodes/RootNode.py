"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

import source.Nodes.ScopedNode as ScopedNode


class RootNode(ScopedNode.ScopedNode):
    """
    The root of our program. Root is a ScopedNode, the base scope of our C program.
    """
    label = "Root"

    def __init__(self):
        super().__init__()

    def resolve_expression(self):
        """ Doesn't doe anything, root is special"""
        pass
