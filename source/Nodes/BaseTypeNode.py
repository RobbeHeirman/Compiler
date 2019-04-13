"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from source.Nodes.LeafNode import LeafNode
from source.Specifiers import TypeSpecifier


class BaseTypeNode(LeafNode):

    _value: TypeSpecifier

    def __init__(self, parent_node, value: TypeSpecifier, filename: str, line: int, column: int):
        """
        Initializer
        :param parent_node: parent node.
        :param value: yield of declarator.
        :param filename: name of file yield is found.
        :param line: line where yield is found.
        :param column: place on line yield is found.
        """
        super().__init__(parent_node, value, filename, line, column)

    @property
    def label(self) -> str:
        return self._value.value

    @property
    def value(self)-> TypeSpecifier:
        return self._value
