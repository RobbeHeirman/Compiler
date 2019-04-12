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

    def __init__(self, parent_node,  value):
        super().__init__(parent_node)
        self._value = value

    @property
    def value(self):
        return self._value