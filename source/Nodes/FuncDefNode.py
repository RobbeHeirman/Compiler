"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.ScopedNode import ScopedNode


class FuncDefNode(ScopedNode):
    label = "function"

    def __init__(self, parent_node):
        super().__init__(parent_node)
