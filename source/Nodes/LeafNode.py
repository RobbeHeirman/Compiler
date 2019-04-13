"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC

from source.Nodes.AbstractNode import AbstractNode


class LeafNode(AbstractNode, ABC):
    """
    Represents all leaf nodes
    """

    def __init__(self, parent_node, value, filename: str, line: int, column: int):
        """
        Initializer
        :param parent_node: the parent node
        :param value: the yield of this leaf node
        :param filename: the filename of this node
        :param column: the column, (place on the line yield is found.)
        :param line:  line yield is found
        """
        super().__init__(parent_node)
        self._line = line
        self._column = column
        self._filename = filename
        self._value = value

    @property
    def value(self):
        return self._value

    @property
    def filename(self):
        return self._filename

    @property
    def line(self):
        return self._line

    @property
    def column(self):
        return self._column
