"""
Author: Robbe Heirman
Project: Simple C Compiler
Academic Year: 2018-2019
"""
from abc import ABC
from typing import List

import Nodes.AbstractNodes.AbstractNode as AbstractNode


class NonLeafNode(AbstractNode.AbstractNode, ABC):
    """
    Abstract node for all intermediate "expression" nodes. Complements leaf node
    """
    _failed: bool
    _children: List["AbstractNode"]

    def __init__(self, parent_node=None):
        super().__init__(parent_node)

        self.type_stack = []

    def dot_string(self) -> str:
        """Generates the visual representation of the node in .dot"""
        ret = super().dot_string()
        ret += "{0}--{{".format(self._index)
        for child in self._children:
            ret += "{0} ".format(child.index)

        ret += "}\n"

        for child in self._children:
            ret += child.dot_string()

        return ret

    def generate_llvm(self) -> str:
        """
        Generates the corresponding node into llvm instructions.
        :return: generates the instructions as a string
        """
        ret = ""
        for child in self._children:
            ret += child.generate_llvm()

        return ret
