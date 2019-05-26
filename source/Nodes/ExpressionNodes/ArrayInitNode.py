"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from Nodes.AbstractNodes.NonLeafNode import NonLeafNode


class ArrayInitNode(NonLeafNode):
    label = "Array Init"

    def __init__(self, parent_node):
        super().__init__(parent_node)
