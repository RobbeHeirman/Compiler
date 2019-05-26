"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""

from Nodes.AbstractNodes.NonLeafNode import NonLeafNode
from Specifiers import TypeSpecifier


class ReturnNode(NonLeafNode):
    label = "return"

    def __init__(self, parent_node: NonLeafNode):
        super().__init__(parent_node)

    @property
    def base_type(self):
        return TypeSpecifier.DEFAULT
