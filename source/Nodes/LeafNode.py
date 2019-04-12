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

    def __init__(self, value):
        super().__init__()
        self._value = value