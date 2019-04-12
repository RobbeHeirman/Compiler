"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.LeafNode import LeafNode
from source.Specifiers import TypeSpecifier


class BaseTypeNode(LeafNode):

    def __init__(self, value: TypeSpecifier):
        super().__init__(value)

    def _label(self):
        return self._value.value
